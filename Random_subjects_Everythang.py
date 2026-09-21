import json
import os
import random
import re
from datetime import datetime, timedelta

# ---------------------------------------------------------
# Supported Print-on-Demand Aspect Ratios
# ---------------------------------------------------------

POD_ASPECT_RATIOS = {
    "1:1": "Square: Mugs, coasters, tote bags, patches, stickers",
    "4:5": "Standard Vertical: Apparel (T-shirts/hoodies), 8x10/16x20 prints",
    "3:4": "Mid Vertical: Canvas wall art, notebooks, posters",
    "9:16": "Tall Vertical: Phone cases, tall tumblers, water bottles",
    "16:9": "Wide Landscape: Desk mats, mousepads, horizontal canvas",
    "2:1": "Panoramic Landscape: Full-wrap ceramic mugs, wide banners",
}

# ---------------------------------------------------------
# Expanded Creative Component Pools
# ---------------------------------------------------------

STYLES = [
    "Synthwave vector illustration with clean neon linework",
    "Cyberpunk technical concept art with sharp outlines",
    "Risograph print style with deliberate ink misregistration",
    "Vintage Japanese woodblock Ukiyo-e print aesthetic",
    "90s retro anime cel-shaded graphic art",
    "Distressed vintage screen-print wash with crackle texture",
    "Bauhaus modernist geometric layout",
    "High-contrast technical blueprint schematic",
    "Dark botanical copperplate engraving",
    "Low-poly faceted geometric illustration",
    "Retro pop art halftone dot screenprint",
    "Minimalist ink wash and brush calligraphy",
]

PALETTES = [
    "Vibrant magenta, electric cyan, and deep midnight navy",
    "Sunset gradient of fiery orange, crimson, and ultraviolet",
    "Monochromatic black, charcoal gray, and crisp white",
    "Earthy sage green, muted terracotta, and warm ochre",
    "Acid green, stark pitch black, and metallic silver",
    "Pastel mint, washed coral, and soft golden yellow",
    "Rustic amber, burnt sienna, and deep forest pine",
    "Cybernetic gold, cobalt blue, and brushed gunmetal",
    "Lavender dusk, soft peach, and deep slate violet",
    "Crimson red, parchment ivory, and sumi ink black",
]

LIGHTING = [
    "Intense dual-tone rim lighting with neon bounce glow",
    "High-contrast chiaroscuro with deep dramatic cast shadows",
    "Low golden-hour sunset backlighting and sun flares",
    "Diffused volumetric lighting filtering through haze and mist",
    "Underlit neon glow casting sharp upward dramatic shadows",
    "Harsh midday cinematic direct light with deep blacks",
    "Soft ambient bioluminescent glow illuminating edges",
]

FINISHES = [
    "Subtle halftone dot shading and faint CRT scanline texture",
    "Distressed vintage wash with light textile wear and crackle",
    "Crisp razor-sharp digital vectors with zero texture",
    "Slight ink-bleed edges and raw cotton paper grain",
    "Matte finish with fine photographic 35mm film grain",
    "Offset color layers with analog print misregistration",
]

# ---------------------------------------------------------
# Dynamic Holiday Date Resolvers
# ---------------------------------------------------------

def get_nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> datetime:
    first_day = datetime(year, month, 1)
    day_offset = (weekday - first_day.weekday()) % 7
    first_occurrence = first_day + timedelta(days=day_offset)
    return first_occurrence + timedelta(weeks=n - 1)


def get_last_weekday_of_month(year: int, month: int, weekday: int) -> datetime:
    next_month = datetime(year + 1, 1, 1) if month == 12 else datetime(year, month + 1, 1)
    last_day = next_month - timedelta(days=1)
    day_offset = (last_day.weekday() - weekday) % 7
    return last_day - timedelta(days=day_offset)


def get_calendar_events_for_year(year: int) -> list[tuple[datetime, str]]:
    october_thanksgiving = get_nth_weekday_of_month(year, 10, 0, 2)
    november_thanksgiving = get_nth_weekday_of_month(year, 11, 3, 4)
    memorial_day = get_last_weekday_of_month(year, 5, 0)
    victoria_day = datetime(year, 5, 24) - timedelta(days=(datetime(year, 5, 24).weekday() + 7) % 7)

    return [
        (datetime(year, 1, 1), "New Year Celebration"),
        (datetime(year, 2, 14), "Valentine's Day"),
        (datetime(year, 3, 17), "St. Patrick's Day"),
        (datetime(year, 4, 15), "Spring Equinox & Easter"),
        (victoria_day, "Victoria Day & National Patriots' Day"),
        (memorial_day, "Memorial Day"),
        (datetime(year, 6, 19), "Juneteenth"),
        (datetime(year, 6, 21), "Summer Solstice & Festival Season"),
        (datetime(year, 6, 24), "La Fête nationale du Québec (Saint-Jean-Baptiste)"),
        (datetime(year, 7, 1), "Canada Day"),
        (datetime(year, 7, 4), "Independence Day (4th of July)"),
        (datetime(year, 9, 30), "National Day for Truth and Reconciliation"),
        (october_thanksgiving, "Thanksgiving & Harvest Season"),
        (datetime(year, 10, 31), "Halloween & Autumnal Gothic"),
        (datetime(year, 11, 11), "Remembrance Day / Veterans Day (11 Nov)"),
        (november_thanksgiving, "Thanksgiving & Harvest Season"),
        (datetime(year, 12, 25), "Winter Solstice & Holiday Season"),
    ]


# ---------------------------------------------------------
# Expanded Subject Libraries
# ---------------------------------------------------------

SEASONAL_SUBJECTS = {
    "Thanksgiving & Harvest Season": [
        "Stylized geometric autumn leaf embedded in a rustic harvest wreath",
        "Vintage cottage cabin surrounded by fiery red, amber, and golden sugar maples",
        "Retro woodland deer standing in misty golden-hour harvest light",
        "Abundant cornucopia with heirloom pumpkins, wheat sheaves, and wild berries",
        "Minimalist botanical line art of dried wheat, acorns, and fall foliage",
        "Steaming spiced cider mug surrounded by cinnamon sticks and autumn flora",
    ],
    "Remembrance Day / Veterans Day (11 Nov)": [
        "Single crimson remembrance poppy rendered in detailed woodblock linework",
        "Field of vibrant scarlet poppies blooming under soft twilight skies",
        "Minimalist commemorative soldier silhouette framed by crimson floral wreath",
        "Vintage pocket watch surrounded by fallen poppy petals and brass gears",
    ],
    "Canada Day": [
        "Bold geometric maple leaf emblem with subtle topographic contour lines",
        "Majestic loon gliding across tranquil northern lake with pine reflections",
        "Vintage retro travel poster silhouette of mountain peaks and glacial water",
        "Stylized polar bear beneath dramatic northern lights ribbons",
    ],
    "Independence Day (4th of July)": [
        "Vintage distressed bald eagle emblem with geometric star patterns",
        "Retro-wave fireworks bursting over a stylized neon city skyline",
        "Distressed patriotic typographic emblem with stars and linear rays",
    ],
    "La Fête nationale du Québec (Saint-Jean-Baptiste)": [
        "Modern fleur-de-lys graphic emblem styled with clean Nordic vectors",
        "Bioluminescent white lily illuminated against midnight blue backdrop",
        "Stylized Saint Lawrence river landscape with flying snowy owl",
    ],
    "Victoria Day & National Patriots' Day": [
        "Vintage Victorian botanical crown intertwined with northern wildflowers",
        "Spring awakening graphic with budding fiddlehead ferns and birch trees",
    ],
    "Halloween & Autumnal Gothic": [
        "Cyber-gothic jack-o'-lantern with glowing mechanical core",
        "Eldritch raven perched on a weathered headstone under full moon",
        "Haunted Victorian mansion silhouette framed by dead twisted branches",
        "Spooky black cat with glowing eyes walking across a witch's apothecary shelf",
        "Anatomical skull sprouting dried nightshade and thorny vines",
    ],
    "Winter Solstice & Holiday Season": [
        "Frost-covered robotic reindeer in a snow-covered pine forest",
        "Cosmic winter snowflake with intricate geometric fractals",
        "Cozy alpine cabin beneath vibrant dancing aurora borealis",
        "Staggered mountain ridge blanketed in deep snow under starry sky",
    ],
    "Valentine's Day": [
        "Anatomical chrome heart entwined with neon digital roses",
        "Twin celestial foxes forming a glowing heart loop",
        "Ornate stained-glass rose window with bleeding heart motifs",
    ],
    "Default Holiday": [
        "Commemorative celebratory emblem with intricate cultural patterns",
        "Constellation star map themed around seasonal transition",
    ],
}

NICHE_PRE_SUMMER_SUBJECTS = [
    # Fitness & Outdoors
    "Stylized kettlebell forged from dark volcanic stone with glowing runes",
    "Retro runner silhouette breaking through a wireframe horizon line",
    "Minimalist mountain trail elevation map with topo lines and compass rose",
    "Anatomical muscular heart entwined with barbell knurling patterns",
    # Pets & Wildlife
    "Anthropomorphic street-smart Doberman wearing a leather rider jacket",
    "Cybernetic cat lounging on top of an 80s arcade monitor",
    "Geometric origami Shiba Inu surrounded by floating sakura petals",
    "Majestic peregrine falcon in mid-dive with geometric air-stream ribbons",
    # Tech & Maker
    "Exploded isometric blueprint diagram of a mechanical keyboard",
    "Microcontroller circuit board layout styled as a cyberpunk metropolis",
    "Vintage dual-cassette deck with exposed gears and magnetic tape loops",
    "Mechanical robotic hand delicately holding a single cherry blossom",
]

TRENDING_POP_CULTURE_SUBJECTS = [
    "1980s retro muscle car drifting along an abandoned highway",
    "Solitary deep-space astronaut tethered to a crumbling cosmic monolith",
    "Mecha samurai standing in defensive stance with energy katana",
    "Bioluminescent alien fungi garden inside a crashed spaceship cargo bay",
    "Minimalist brutalist concrete tower under a dying red giant star",
    "Futuristic toroidal space station orbiting a ringed exoplanet",
    "Cyberpunk street vendor stall glowing with neon signs in the rain",
    "Steampunk airship navigating treacherous lightning clouds",
    "Low-poly robotic wolf howling atop a neon grid cliff",
    "Retro arcade claw machine filled with floating cosmic planets",
    "Submerged futuristic metropolis seen through deep ocean waters",
    "Synthwave road trip van parked beneath twin full moons",
]

NEGATIVE_PROMPT_DEFAULT = (
    "low quality, blurry, photorealistic human skin, low resolution, "
    "messy borders, unwanted text, watermark, signature, artifacting, noisy background"
)


# ---------------------------------------------------------
# Context Evaluator & Diversity Selector
# ---------------------------------------------------------

def evaluate_calendar_context(current_date: datetime) -> tuple[str, str, str, str | None]:
    year = current_date.year
    calendar_events = get_calendar_events_for_year(year) + get_calendar_events_for_year(year + 1)

    for event_date, event_name in calendar_events:
        days_until = (event_date - current_date).days
        if 30 <= days_until <= 45:
            burst_duration = random.randint(2, 5)
            if (45 - days_until) < burst_duration:
                subject_pool = SEASONAL_SUBJECTS.get(
                    event_name, SEASONAL_SUBJECTS["Default Holiday"]
                )
                subject = random.choice(subject_pool)
                context = f"Commemorative theme for upcoming {event_name}"
                return "Seasonal / Calendar Event", subject, context, event_name

    if current_date.month in [12, 1, 2, 3]:
        subject = random.choice(NICHE_PRE_SUMMER_SUBJECTS)
        context = "Pre-summer active prep niche (fitness, pets, and maker tech focus)"
        return "Pre-Summer Niche Calendar", subject, context, None

    subject = random.choice(TRENDING_POP_CULTURE_SUBJECTS)
    context = "High-engagement evergreen pop culture & sci-fi aesthetic"
    return "Pop Culture / Web Trends", subject, context, None


def sanitize_folder_name(name: str) -> str:
    cleaned = re.sub(r"[\\/*?:\'\"<>|&,()]+", " ", name)
    return "_".join(cleaned.split()).strip("_")


def pick_diverse_choice(pool: list[str], recent_history: list[str]) -> str:
    """Picks a value avoiding the most recent historical entries when possible."""
    available = [item for item in pool if item not in recent_history]
    return random.choice(available if available else pool)


# ---------------------------------------------------------
# Model Generator & Storage Pipeline
# ---------------------------------------------------------

def generate_pod_model(
    recent_history: dict | None = None,
    target_date: datetime | None = None,
) -> dict:
    ref_date = target_date or datetime.now()
    trigger_type, base_subject, context_desc, event_name = evaluate_calendar_context(ref_date)

    recent = recent_history or {"subjects": [], "styles": [], "palettes": []}

    # Ensure variation by checking past outputs
    if trigger_type == "Pop Culture / Web Trends":
        subject = pick_diverse_choice(TRENDING_POP_CULTURE_SUBJECTS, recent["subjects"])
    elif trigger_type == "Pre-Summer Niche Calendar":
        subject = pick_diverse_choice(NICHE_PRE_SUMMER_SUBJECTS, recent["subjects"])
    else:
        subject = base_subject

    style = pick_diverse_choice(STYLES, recent["styles"])
    palette = pick_diverse_choice(PALETTES, recent["palettes"])
    lighting = random.choice(LIGHTING)
    finish = random.choice(FINISHES)

    base_art_directive = (
        f"{style}, {subject}. Setting: {context_desc}. "
        f"Color palette: {palette}. Lighting: {lighting}. Texture: {finish}. "
        f"Commercial graphic quality, clear silhouette, vector clarity."
    )

    aspect_ratio_variations = {}
    for ratio, description in POD_ASPECT_RATIOS.items():
        aspect_ratio_variations[ratio] = {
            "aspect_ratio": ratio,
            "target_products": description,
            "prompt": f"{base_art_directive} Formatted for {ratio} composition with balanced canvas margins.",
        }

    return {
        "id": None,
        "timestamp": ref_date.isoformat(),
        "event_name": event_name,
        "context_engine": {
            "trigger_type": trigger_type,
            "context_detail": context_desc,
        },
        "negative_prompt": NEGATIVE_PROMPT_DEFAULT,
        "design_parameters": {
            "subject": subject,
            "style": style,
            "palette": palette,
            "lighting": lighting,
            "finish": finish,
        },
        "aspect_ratio_variations": aspect_ratio_variations,
    }


def export_daily_pod_model(
    base_dir: str = "models",
    target_date: datetime | None = None,
) -> None:
    ref_date = target_date or datetime.now()
    _, _, _, event_name = evaluate_calendar_context(ref_date)

    folder_name = f"Seasonal_{sanitize_folder_name(event_name)}" if event_name else "General"
    target_folder = os.path.join(base_dir, folder_name)
    os.makedirs(target_folder, exist_ok=True)

    filepath = os.path.join(target_folder, "prompts.json")

    existing_data = []
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                existing_data = json.load(f)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
        except (json.JSONDecodeError, IOError):
            existing_data = []

    # Gather recent choices from the last 5 entries to guarantee novelty
    last_entries = existing_data[-5:]
    recent_history = {
        "subjects": [e["design_parameters"]["subject"] for e in last_entries if "design_parameters" in e],
        "styles": [e["design_parameters"]["style"] for e in last_entries if "design_parameters" in e],
        "palettes": [e["design_parameters"]["palette"] for e in last_entries if "design_parameters" in e],
    }

    model = generate_pod_model(recent_history=recent_history, target_date=ref_date)
    model["id"] = len(existing_data) + 1
    existing_data.append(model)

    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(existing_data, f, indent=2, ensure_ascii=False)

    print(f"Exported model #{model['id']} [{model['context_engine']['trigger_type']}]")
    print(f"Subject: {model['design_parameters']['subject']}")
    print(f"Style:   {model['design_parameters']['style']}")
    print(f"Palette: {model['design_parameters']['palette']}")
    print(f"Saved to: {filepath}\n")


if __name__ == "__main__":
    export_daily_pod_model()