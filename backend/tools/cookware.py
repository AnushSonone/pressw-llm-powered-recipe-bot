"""
Cookware checker: validate whether the user can make a recipe with their available tools.
Uses the hardcoded list from the spec (assume this is what the user has).
"""

import logging

from langchain_core.tools import tool

logger = logging.getLogger(__name__)

USER_COOKWARE = [
    "Spatula",
    "Frying Pan",
    "Little Pot",
    "Stovetop",
    "Whisk",
    "Knife",
    "Ladle",
    "Spoon",
]


@tool
def check_cookware(required_equipment: str) -> str:
    """
    Check if the user has the equipment needed for a recipe.
    Input: comma-separated list of required tools/equipment (e.g. "Frying Pan, Knife, Bowl").
    Returns whether they can cook it and lists any missing items.
    """
    required = [s.strip() for s in required_equipment.split(",") if s.strip()]
    available_lower = {s.lower(): s for s in USER_COOKWARE}
    missing = []
    for r in required:
        if not r:
            continue
        r_lower = r.lower()
        if r_lower not in available_lower:
            missing.append(r)
    if not missing:
        logger.info("check_cookware: user has all required equipment")
        return "The user has all required equipment and can make this recipe."
    logger.info("check_cookware: missing %s", missing)
    return (
        f"The user is missing: {', '.join(missing)}. "
        "They have: " + ", ".join(USER_COOKWARE) + ". "
        "Suggest a substitute or a simpler version if possible."
    )
