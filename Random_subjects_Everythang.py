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
# Modular Creative Component Pools
# ---------------------------------------------------------

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

PALETTES = [
    "Vibrant magenta, electric cyan, and deep midnight navy",
    "Sunset gradient of fiery orange, crimson, and ultraviolet",
    "Monochromatic black, charcoal gray, and crisp white",
    "Earthy sage green, muted terracotta, and warm ochre",
    "Acid green, stark black, and metallic silver",
    "Pastel mint, washed coral, and soft golden yellow",
    "Rustic amber, burnt sienna, and deep forest pine",
]

LIGHTING = [
    "Intense rim lighting with vibrant neon bounce glow",
    "High-contrast chiaroscuro with deep dramatic shadows",
    "Low golden-hour sunset backlighting",
    "Diffused volumetric lighting filtering through haze",
    "Underlit neon glow casting sharp upward shadows",
]

FINISHES = [
    "Subtle halftone dot shading and faint CRT scanline texture",
    "Distressed vintage wash with light textile wear and crackle",
    "Crisp razor-sharp digital vectors with zero texture",
    "Slight ink-bleed edges and raw cotton paper grain",
    "Matte finish with fine photographic film grain",
]

# ---------------------------------------------------------
# Date Helper Functions for Floating Holidays
# ---------------------------------------------------------

def get_nth_weekday_of_month(year: int, month: int, weekday: int, n: int) -> datetime:
    """Returns the nth weekday of a given month (0 = Monday, 6 = Sunday)."""
    first_day = datetime(year, month, 1)
    day_offset = (weekday - first_day.weekday()) % 7
    first_occurrence = first_day + timedelta(days=day_offset)
    return first_occurrence + timedelta(weeks=n - 1)


def get_last_weekday_of_month(year: int, month: int, weekday: int) -> datetime:
    """Returns the last occurrence of a given weekday in a month."""
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    last_day = next_month - timedelta(days=1)
    day_offset = (last_day.weekday() - weekday) % 7
    return last_day - timedelta(days=day_offset)


def get_calendar_events_for_year(year: int) -> list[tuple[datetime, str]]:
    """Builds a unified list of calendar events without national tags on Thanksgiving."""
    october_thanksgiving = get_nth_weekday_of_month(year, 10, 0, 2)   # 2nd Monday of Oct
    november_thanksgiving = get_nth_weekday_of_month(year, 11, 3, 4)  # 4th Thursday of Nov
    memorial_day = get_last_weekday_of_month(year, 5, 0)
    victoria_day = datetime(year, 5, 24) - timedelta(days=(datetime(year, 5, 24).weekday() + 7) % 7)

    events = [
        # Fixed Winter / Spring
        (datetime(year, 1, 1), "New Year Celebration"),
        (datetime(year, 2, 14), "Valentine's Day"),
        (datetime(year, 3, 17), "St. Patrick's Day"),
        (datetime(year, 4, 15), "Spring Equinox & Easter"),
        
        # Spring / Early Summer Regional & National
        (victoria_day, "Victoria Day & National Patriots' Day"),
        (memorial_day, "Memorial Day"),
        (datetime(year, 6, 19), "Juneteenth"),
        (datetime(year, 6, 21), "Summer Solstice & Festival Season"),
        (datetime(year, 6, 24), "La Fête nationale du Québec (Saint-Jean-Baptiste)"),
        
        # Mid-Summer Days
        (datetime(year, 7, 1), "Canada Day"),
        (datetime(year, 7, 4), "Independence Day (4th of July)"),
        
        # Autumn National, Cultural & Regional
        (datetime(year, 9, 30), "National Day for Truth and Reconciliation"),
        (october_thanksgiving, "Thanksgiving & Harvest Season"),
        (datetime(year, 10, 31), "Halloween & Autumnal Gothic"),
        (datetime(year, 11, 11), "Remembrance Day / Veterans Day (11 Nov)"),
        (november_thanksgiving, "Thanksgiving & Harvest Season"),
        
        # Winter Holidays
        (datetime(year, 12, 25), "Winter Solstice & Holiday Season"),
    ]
    return events


# ---------------------------------------------------------
# Event-Specific Thematic Subject Pools
# ---------------------------------------------------------

SEASONAL_SUBJECTS = {
    "Thanksgiving & Harvest Season": [
        "Stylized geometric autumn leaf embedded in a rustic harvest wreath",
        "Vintage cottage cabin surrounded by fiery red, amber, and golden sugar maples",
        "Retro woodland deer standing in misty golden-hour harvest light",
        "Abundant cornucopia with heirloom pumpkins, wheat sheaves, and wild berries",
        "Minimalist botanical line art of dried wheat, acorns, and fall foliage",
    ],
    "Remembrance Day / Veterans Day (11 Nov)": [
        "Single crimson remembrance poppy rendered in detailed woodblock linework",
        "Field of vibrant scarlet poppies blooming under soft twilight skies",
        "Minimalist commemorative soldier silhouette framed by crimson floral wreath",
    ],
    "Canada Day": [
        "Bold geometric maple leaf emblem with subtle topographic contour lines",
        "Majestic loon gliding across tranquil northern lake with pine reflections",
        "Vintage retro travel poster silhouette of mountain peaks and glacial water",
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
    ],
    "Winter Solstice & Holiday Season": [
        "Frost-covered robotic reindeer in a snow-covered pine forest",
        "Cosmic winter snowflake with intricate geometric fractals",
        "Cozy alpine cabin beneath vibrant dancing aurora borealis",
    ],
    "Valentine's Day": [
        "Anatomical chrome heart entwined with neon digital roses",
        "Twin celestial foxes forming a glowing heart loop",
    ],
    "Default Holiday": [
        "Commemorative celebratory emblem with intricate cultural patterns",
        "Constellation star map themed around seasonal transition",
    ],
}

NICHE_PRE_SUMMER_SUBJECTS = [
    # Fitness
    "Stylized kettlebell forged from dark volcanic stone with glowing runes",
    "Retro runner silhouette breaking through a wireframe horizon line",
    "Minimalist mountain trail elevation map with topo lines",
    # Pets
    "Anthropomorphic street-smart Doberman wearing a leather rider jacket",
    "Cybernetic cat lounging on top of an 80s arcade monitor",
    "Geometric origami Shiba Inu surrounded by floating sakura petals",
    # Tech & Maker
    "Exploded isometric blueprint diagram of a mechanical keyboard",
    "Microcontroller circuit board layout styled as a cyberpunk metropolis",
    "Vintage dual-cassette deck with exposed gears and magnetic tape loops",
]

TRENDING_POP_CULTURE_SUBJECTS = [
    "1980s retro muscle car drifting along an abandoned highway",
    "Solitary astronaut floating in a deep space rift",
    "Mecha samurai standing in defensive stance with energy katana",
    "Bioluminescent alien fungi garden on an asteroid",
    "Minimalist brutalist concrete monument under a dying red giant star",
    "Futuristic toroidal space station orbiting a ringed exoplanet",
]

NEGATIVE_PROMPT_DEFAULT = (
    "low quality, blurry, photorealistic human skin, low resolution, "
    "messy borders, unwanted text, watermark, signature, artifacting, noisy background"
)


# ---------------------------------------------------------
# Dynamic Context Selector & File Utils
# ---------------------------------------------------------

def evaluate_calendar_context(current_date: datetime) -> tuple[str, str, str, str | None]:
    """
    Evaluates context:
    1. Seasonal shifts & Regional/National events (30 to 45 days prior, running 2-5 days).
    2. Niche calendars (Dec - Mar, ~6 months before summer).
    3. Pop culture / trending fallback.

    Returns: (trigger_type, subject, context_detail, event_name_or_none)
    """
    year = current_date.year
    calendar_events = get_calendar_events_for_year(year) + get_calendar_events_for_year(year + 1)

    # 1. Seasonal Shifts & Regional/National events
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

    # 2. Niche-Specific Calendars: 6 months before summer (Dec, Jan, Feb, Mar)
    if current_date.month in [12, 1, 2, 3]:
        subject = random.choice(NICHE_PRE_SUMMER_SUBJECTS)
        context = "Pre-summer active prep niche (fitness, pets, and maker tech focus)"
        return "Pre-Summer Niche Calendar", subject, context, None

    # 3. Fallback: Pop Culture / Trends
    subject = random.choice(TRENDING_POP_CULTURE_SUBJECTS)
    context = "High-engagement evergreen pop culture & sci-fi aesthetic"
    return "Pop Culture / Web Trends", subject, context, None


def sanitize_folder_name(name: str) -> str:
    """Converts a descriptive string into a safe directory path name."""
    cleaned = re.sub(r"[\\/*?:\'\"<>|&,()]+", " ", name)
    cleaned = "_".join(cleaned.split())
    return cleaned.strip("_")


# ---------------------------------------------------------
# Model Generator & Local Storage Exporter
# ---------------------------------------------------------

def generate_pod_model(
    design_id: int | None = None, target_date: datetime | None = None
) -> dict:
    """Generates a daily design model with prompts formatted across all 6 POD aspect ratios."""
    ref_date = target_date or datetime.now()
    trigger_type, subject, context_desc, event_name = evaluate_calendar_context(ref_date)

    style = random.choice(STYLES)
    palette = random.choice(PALETTES)
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
        "id": design_id or random.randint(1000, 9999),
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
    """
    Generates a daily model, checks if the target folder exists, creates it if not,
    and appends the model to the folder's prompts.json file.
    """
    model = generate_pod_model(target_date=target_date)
    event_name = model.get("event_name")

    # 1. Resolve folder name
    if event_name:
        folder_name = f"Seasonal_{sanitize_folder_name(event_name)}"
    else:
        folder_name = "General"

    # 2. Build target path
    target_folder = os.path.join(base_dir, folder_name)

    # 3. Create folder hierarchy automatically if it doesn't exist
    os.makedirs(target_folder, exist_ok=True)

    filepath = os.path.join(target_folder, "prompts.json")

    # 4. Load or initialize JSON records
    existing_data = []
    if os.path.exists(filepath):
        try:
            with open(filepath, "r", encoding="utf-8") as file:
                existing_data = json.load(file)
                if not isinstance(existing_data, list):
                    existing_data = [existing_data]
        except (json.JSONDecodeError, IOError):
            existing_data = []

    model["id"] = len(existing_data) + 1
    existing_data.append(model)

    # 5. Save back to disk
    with open(filepath, "w", encoding="utf-8") as file:
        json.dump(existing_data, file, indent=2, ensure_ascii=False)

    print(f"Exported model #{model['id']} ({model['context_engine']['trigger_type']}) -> {filepath}")


if __name__ == "__main__":
    export_daily_pod_model()