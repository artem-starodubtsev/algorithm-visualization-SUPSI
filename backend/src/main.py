from pathlib import Path
from typing import Any
import importlib
import inspect

from fastapi import FastAPI, HTTPException
import uvicorn
from pydantic import ValidationError

app = FastAPI()

MODULES_DIR = Path("modules")


def build_tree(root: Path) -> list[dict[str, Any]]:
    def walk(dir_path: Path) -> list[dict[str, Any]]:
        nodes: list[dict[str, Any]] = []
        for p in sorted(dir_path.iterdir()):
            if p.name.startswith("_"):
                continue
            if p.is_dir():
                nodes.append(
                    {
                        "name": p.name,
                        "children": walk(p),
                    }
                )
            elif p.suffix == ".py" and p.name != "__init__.py":
                nodes.append(
                    {
                        "name": p.stem,
                    }
                )
        return nodes

    return walk(root)


@app.get("/modules")
def list_modules():
    return build_tree(MODULES_DIR)


def get_algos(module_path: str) -> Any:
    target = MODULES_DIR / (module_path + ".py")
    name = module_path.split("/")[-1]

    try:
        target.relative_to(MODULES_DIR)
    except ValueError:
        raise HTTPException(status_code=404, detail="Module not found")

    if not target.is_file():
        raise HTTPException(status_code=404, detail="Module not found")

    import_path = "modules." + module_path.replace("/", ".").replace("\\", ".")

    try:
        module = importlib.import_module(import_path)
    except ModuleNotFoundError:
        raise HTTPException(status_code=404, detail="Module not found")

    try:
        AlgoCls = getattr(module, name + "Algorithm")
        AlgoInstanceCls = getattr(module, name + "Instance")
    except AttributeError:
        raise HTTPException(status_code=404, detail="GaleShapleyAlgorithm not found in module")

    return AlgoCls, AlgoInstanceCls


@app.get("/modules/{module_path:path}")
def get_single_module(module_path: str):
    return get_algos(module_path)[0]().input_scheme()


@app.post("/modules/{module_path:path}")
def run_algorithm(module_path: str, payload: dict[str, Any]):
    AlgoCls, AlgoInstanceCls = get_algos(module_path)
    algo = AlgoCls()
    try:
        instance = AlgoInstanceCls(**payload)
    except ValidationError as e:
        raise HTTPException(
            status_code=400,
            detail='\n'.join([f'{i}. {error['msg']}' for i, error in enumerate(e.errors(), 1)]),
        )

    try:
        result = algo.solve(instance)
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=str(e),
        )
    return result.model_dump()


if __name__ == "__main__":
    # This runs when you do: python main.py
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,  # auto-reload on code changes (dev only)
    )
