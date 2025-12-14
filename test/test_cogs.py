import importlib
import pytest
import os

COGS_DIR = os.path.join(os.path.dirname(__file__), "..", "teapot", "cogs")
COGS = [
    fname[:-3] for fname in os.listdir(COGS_DIR)
    if fname.endswith(".py") and fname != "__init__.py"
]

@pytest.mark.parametrize("cog_name", COGS)
def test_cog_import_and_setup(cog_name):
    mod_path = f"teapot.cogs.{cog_name}"
    module = importlib.import_module(mod_path)
    # check for cog class
    cog_class = None
    for attr in dir(module):
        obj = getattr(module, attr)
        if hasattr(obj, "__bases__") and any(b.__name__ == "Cog" for b in getattr(obj, "__bases__", [])):
            cog_class = obj
            break
    assert cog_class is not None, f"{mod_path} Does not have a valid Cog class"
    assert hasattr(module, "setup"), f"{mod_path} is missing setup(bot) function"
    assert callable(getattr(module, "setup")), f"{mod_path} setup is not a callable function"
