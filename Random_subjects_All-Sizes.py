import json
import os
import random
from datetime import datetime

# ---------------------------------------------------------
# Supported Standard POD Aspect Ratios
# ---------------------------------------------------------

POD_ASPECT_RATIOS = [
    "1:1",   # Square: Mugs, coasters, tote bags, patches, stickers
    "4:5",   # Standard Vertical: Apparel (T-shirts/hoodies), 8x10/16x20 prints
    "3:4",   # Mid Vertical: Canvas wall art, notebooks, posters
    "9:16",  # Tall Vertical: Phone cases, tall tumblers, water bottles
    "16:9",  # Wide Landscape: Desk mats, mousepads, horizontal canvas
    "2:1",   # Panoramic Landscape: Full-wrap ceramic mugs, wide banners
]

# ---------------------------------------------------------
# Parameter Pools (Decoupled from layout & framing)
# ---------------------------------------------------------

SUBJECTS = [
    "Cyberpunk street racer with glowing visor",
    "1980s retro muscle car drifting",
    "Solitary astronaut floating in deep space",
    "Bioluminescent alien flora and giant mushrooms",
    "Mecha samurai standing in defensive stance",
    "Anthropomorphic urban fox wearing streetwear",
    "Vintage modular analog synthesizer covered in cables",
    "Minimalist brutalist concrete monument",
    "Futuristic toroidal space station orbiting a ringed planet",
    "Retro arcade cabinet glowing in darkness",
]

STYLES = [
    "Synthwave vector illustration with clean linework",
    "Cyberpunk concept art with hard edge outlines",
    "Risograph print style with subtle misregistration",
    "Vintage woodblock Ukiyo-e print aesthetic",
    "90s retro anime cel shaded graphic",
    "Distressed vintage screen print aesthetic",
    "Bauhaus geometric graphic design",
    "High-contrast technical blueprint schematic",
]

CONTEXTS = [
    "Neon-soaked rainy alleyway with reflective puddles",
    "Desert highway with wireframe grid on the horizon",
    "Deep space void illuminated by a dying supernova",
    "Overgrown solarpunk greenhouse with hanging vines",
    "Dense atmospheric fog under harsh streetlights",
    "Dark minimalist studio stage with directional light",
]

PALETTES = [
    "Vibrant magenta, electric cyan, and deep midnight navy",
    "Sunset gradient of fiery orange, crimson, and ultraviolet",
    "Monochromatic black, charcoal gray, and crisp white",
    "Earthy sage green, muted terracotta, and warm ochre",
    "Acid green, stark black, and metallic silver",
    "Pastel mint, washed coral, and soft golden yellow",
]

LIGHTING = [
    "Intense rim lighting with vibrant neon bounce glow",
    "High-contrast chiaroscuro with deep dramatic shadows",
    "Low golden-hour sunset backlighting",
    "Diffused volumetric lighting filtering through haze",
    "Underlit neon glow casting sharp upward shadows",
]

COMPOSITIONS = [
    "Centered isolated subject on a solid clean background, sharp silhouette edges",
    "Balanced geometric composition, optimized for center-weighted retrofitting",
    "Dynamic layered composition with adaptable focal framing",
]

FINISHES = [
    "Subtle halftone dot shading and faint CRT scanline texture",
    "Distressed vintage wash with light textile wear and crackle",
    "Crisp razor-sharp digital vectors with zero texture",
    "Slight ink-bleed edges and raw cotton paper grain",
    "Matte finish with fine photographic film grain",
]

NEGATIVE_PROMPT_DEFAULT = (
    "low quality, blurry, photorealistic skin, low resolution, messy borders, "
    "unwanted text, watermark, signature, artifacting, noisy background"
)


# ---------------------------------------------------------
# Generator Core
# ---------------------------------------------------------

def generate_pod_design_set(design_id: int | None = None) -> dict:
    """Randomizes design parameters once, then generates outputs for every POD aspect ratio."""
    chosen_subject = random.choice(SUBJECTS)
    chosen_style = random.choice(STYLES)
    chosen_context = random.choice(CONTEXTS)
    chosen_palette = random.choice(PALETTES)
    chosen_lighting = random.choice(LIGHTING)
    chosen_composition = random.choice(COMPOSITIONS)
    chosen_finish = random.choice(FINISHES)

    base_prompt_body = (
        f"{chosen_style}, {chosen_subject}. {chosen_context}. "
        f"Color palette: {chosen_palette}. Lighting: {chosen_lighting}. "
        f"Composition: {chosen_composition}. Texture: {chosen_finish}. "
        f"Vector clarity, commercial graphic design quality."
    )

    # Generate an entry for every ratio using the exact same design parameters
    variants = []
    for ratio in POD_ASPECT_RATIOS:
        variants.append({
            "aspect_ratio": ratio,
            "prompt": f"{base_prompt_body} --ar {ratio}",
            "negative_prompt": NEGATIVE_PROMPT_DEFAULT,
        })

    return {
        "id": design_id or random.randint(1000, 9999),
        "timestamp": datetime.now().isoformat(),
        "design_concept": {
            "subject": chosen_subject,
            "style": chosen_style,
            "context": chosen_context,
            "palette": chosen_palette,
            "lighting": chosen_lighting,
            "composition": chosen_composition,
            "finish": chosen_finish,
        },
        "variants": variants,
    }


def export_prompts_to_json(
    filepath: str = "pod_daily_prompts.json", count: int = 1, append: bool = True
) -> None:
    """Generates multi-ratio design sets and stores them in JSON."""
    existing_data = []

    if append and os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
        except (json.JSONDecodeError, IOError):
            existing_data = []

    new_entries = [
        generate_pod_design_set(design_id=len(existing_data) + i + 1)
        for i in range(count)
    ]
    all_data = existing_data + new_entries

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(all_data, file, indent=2, ensure_ascii=False)

    print(
        f"Generated {len(new_entries)} design concept(s) across "
        f"{len(POD_ASPECT_RATIOS)} aspect ratios each. Saved to '{filepath}'."
    )


if __name__ == "__main__":
    export_prompts_to_json(filepath="pod_daily_prompts.json", count=1, append=True)