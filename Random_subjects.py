import json
import os
import random
from datetime import datetime

# ---------------------------------------------------------
# Parameter Pools
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
    "Contained within a sharp geometric circular emblem",
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
    {
        "desc": "Isolated centered subject on a pure clean solid background, sharp silhouette edges",
        "primary_pod": "T-Shirts, Hoodies, and Die-Cut Stickers",
        "aspect_ratio": "4:5",
    },
    {
        "desc": "Structured circular badge emblem with clean outer boundary and balanced symmetry",
        "primary_pod": "Hats, Mugs, Patches, and Coasters",
        "aspect_ratio": "1:1",
    },
    {
        "desc": "Full-bleed edge-to-edge dynamic wide composition with rich background detail",
        "primary_pod": "Posters, Desk Mats, Canvas Prints, and Phone Cases",
        "aspect_ratio": "16:9",
    },
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

def generate_pod_prompt(design_id: int | None = None) -> dict:
    """Randomizes parameters and builds a unified POD model prompt payload."""
    subject = random.choice(SUBJECTS)
    style = random.choice(STYLES)
    context = random.choice(CONTEXTS)
    palette = random.choice(PALETTES)
    lighting = random.choice(LIGHTING)
    composition = random.choice(COMPOSITIONS)
    finish = random.choice(FINISHES)

    # Synthesize parameters into a coherent diffusion/generation prompt
    prompt_string = (
        f"{style}, {subject}. {context}. Color palette: {palette}. "
        f"Lighting: {lighting}. Composition: {composition['desc']}. "
        f"Texture: {finish}. Vector clarity, commercial graphic design quality."
    )

    return {
        "id": design_id or random.randint(1000, 9999),
        "timestamp": datetime.now().isoformat(),
        "target_product": composition["primary_pod"],
        "aspect_ratio": composition["aspect_ratio"],
        "prompt": prompt_string,
        "negative_prompt": NEGATIVE_PROMPT_DEFAULT,
        "parameters": {
            "subject": subject,
            "style": style,
            "context": context,
            "palette": palette,
            "lighting": lighting,
            "composition": composition["desc"],
            "finish": finish,
        },
    }


def export_prompts_to_json(
    filepath: str = "pod_daily_prompts.json", count: int = 1, append: bool = True
) -> None:
    """Generates prompt entries and exports them formatted to a JSON file."""
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
        generate_pod_prompt(design_id=len(existing_data) + i + 1)
        for i in range(count)
    ]
    all_data = existing_data + new_entries

    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(all_data, file, indent=2, ensure_ascii=False)

    print(f"Successfully wrote {len(new_entries)} prompt(s) to '{filepath}'.")


if __name__ == "__main__":
    # Generate today's single model prompt
    export_prompts_to_json(filepath="pod_daily_prompts.json", count=1, append=True)