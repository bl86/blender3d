"""
Animation configuration presets
Allows easy customization of animation parameters
"""

# Animation timing presets
TIMING_PRESETS = {
    'quick': {
        'total_frames': 150,
        'fire_end_frame': 100,
        'fps': 30,
        'description': 'Quick 5-second reveal'
    },
    'standard': {
        'total_frames': 300,
        'fire_end_frame': 200,
        'fps': 30,
        'description': 'Standard 10-second animation'
    },
    'cinematic': {
        'total_frames': 450,
        'fire_end_frame': 320,
        'fps': 24,
        'description': 'Slow cinematic 18-second reveal'
    },
    'extended': {
        'total_frames': 600,
        'fire_end_frame': 400,
        'fps': 30,
        'description': 'Extended 20-second showcase'
    }
}

# Render quality presets
RENDER_PRESETS = {
    'preview': {
        'samples': 32,
        'resolution_x': 1280,
        'resolution_y': 720,
        'resolution_percentage': 50,
        'use_denoising': True,
        'volume_resolution': 128,
        'description': 'Fast preview quality'
    },
    'draft': {
        'samples': 64,
        'resolution_x': 1920,
        'resolution_y': 1080,
        'resolution_percentage': 75,
        'use_denoising': True,
        'volume_resolution': 128,
        'description': 'Draft quality for review'
    },
    'production': {
        'samples': 256,
        'resolution_x': 1920,
        'resolution_y': 1080,
        'resolution_percentage': 100,
        'use_denoising': True,
        'volume_resolution': 256,
        'description': 'High quality production render'
    },
    'ultra': {
        'samples': 512,
        'resolution_x': 3840,
        'resolution_y': 2160,
        'resolution_percentage': 100,
        'use_denoising': True,
        'volume_resolution': 384,
        'description': '4K ultra quality (slow)'
    }
}

# Material color presets
COLOR_PRESETS = {
    'classic_gold': {
        'base_color': (1.0, 0.766, 0.336, 1.0),
        'emission_color': (1.0, 0.85, 0.4, 1.0),
        'emission_strength': 0.3,
        'roughness': 0.15,
        'description': 'Classic rich gold'
    },
    'rose_gold': {
        'base_color': (0.95, 0.65, 0.55, 1.0),
        'emission_color': (1.0, 0.7, 0.6, 1.0),
        'emission_strength': 0.25,
        'roughness': 0.12,
        'description': 'Elegant rose gold'
    },
    'white_gold': {
        'base_color': (0.95, 0.95, 0.88, 1.0),
        'emission_color': (1.0, 1.0, 0.95, 1.0),
        'emission_strength': 0.2,
        'roughness': 0.1,
        'description': 'Bright white gold'
    },
    'bronze': {
        'base_color': (0.8, 0.5, 0.2, 1.0),
        'emission_color': (0.9, 0.6, 0.3, 1.0),
        'emission_strength': 0.15,
        'roughness': 0.25,
        'description': 'Ancient bronze'
    },
    'silver': {
        'base_color': (0.85, 0.85, 0.88, 1.0),
        'emission_color': (0.95, 0.95, 1.0, 1.0),
        'emission_strength': 0.2,
        'roughness': 0.08,
        'description': 'Polished silver'
    },
    'platinum': {
        'base_color': (0.9, 0.89, 0.88, 1.0),
        'emission_color': (0.95, 0.94, 0.93, 1.0),
        'emission_strength': 0.25,
        'roughness': 0.06,
        'description': 'Premium platinum'
    }
}

# Fire intensity presets
FIRE_PRESETS = {
    'subtle': {
        'fuel_amount': 1.0,
        'temperature': 2.0,
        'velocity_factor': 1.0,
        'emission_strength': 15.0,
        'description': 'Subtle flames'
    },
    'moderate': {
        'fuel_amount': 1.5,
        'temperature': 2.5,
        'velocity_factor': 1.2,
        'emission_strength': 20.0,
        'description': 'Moderate fire'
    },
    'intense': {
        'fuel_amount': 2.0,
        'temperature': 3.0,
        'velocity_factor': 1.5,
        'emission_strength': 25.0,
        'description': 'Intense inferno'
    },
    'extreme': {
        'fuel_amount': 3.0,
        'temperature': 4.0,
        'velocity_factor': 2.0,
        'emission_strength': 35.0,
        'description': 'Extreme blaze'
    }
}

# Camera presets
CAMERA_PRESETS = {
    'standard': {
        'lens': 50,
        'fstop': 2.8,
        'start_distance': 25,
        'end_distance': 5,
        'description': 'Standard 50mm lens'
    },
    'wide': {
        'lens': 35,
        'fstop': 2.0,
        'start_distance': 20,
        'end_distance': 4,
        'description': 'Wide angle 35mm'
    },
    'telephoto': {
        'lens': 85,
        'fstop': 1.8,
        'start_distance': 30,
        'end_distance': 8,
        'description': 'Telephoto 85mm with shallow DOF'
    },
    'dramatic': {
        'lens': 24,
        'fstop': 1.4,
        'start_distance': 15,
        'end_distance': 3,
        'description': 'Dramatic wide angle with bokeh'
    }
}

# Lighting presets
LIGHTING_PRESETS = {
    'studio': {
        'key_energy': 500,
        'fill_energy': 200,
        'rim_energy': 300,
        'ambient_strength': 0.5,
        'description': 'Professional studio lighting'
    },
    'dramatic': {
        'key_energy': 800,
        'fill_energy': 100,
        'rim_energy': 500,
        'ambient_strength': 0.2,
        'description': 'High contrast dramatic'
    },
    'soft': {
        'key_energy': 300,
        'fill_energy': 250,
        'rim_energy': 150,
        'ambient_strength': 0.8,
        'description': 'Soft even lighting'
    },
    'cinematic': {
        'key_energy': 600,
        'fill_energy': 150,
        'rim_energy': 400,
        'ambient_strength': 0.3,
        'description': 'Cinematic mood lighting'
    }
}


def get_preset(category, name):
    """
    Get a specific preset by category and name

    Args:
        category: 'timing', 'render', 'color', 'fire', 'camera', or 'lighting'
        name: preset name

    Returns:
        dict: Preset configuration
    """
    presets = {
        'timing': TIMING_PRESETS,
        'render': RENDER_PRESETS,
        'color': COLOR_PRESETS,
        'fire': FIRE_PRESETS,
        'camera': CAMERA_PRESETS,
        'lighting': LIGHTING_PRESETS
    }

    if category not in presets:
        raise ValueError(f"Unknown category: {category}")

    if name not in presets[category]:
        raise ValueError(f"Unknown preset '{name}' in category '{category}'")

    return presets[category][name]


def list_presets(category=None):
    """
    List available presets

    Args:
        category: Optional category filter

    Returns:
        dict: Available presets
    """
    all_presets = {
        'timing': TIMING_PRESETS,
        'render': RENDER_PRESETS,
        'color': COLOR_PRESETS,
        'fire': FIRE_PRESETS,
        'camera': CAMERA_PRESETS,
        'lighting': LIGHTING_PRESETS
    }

    if category:
        return {category: all_presets.get(category, {})}

    return all_presets


def print_presets():
    """Print all available presets"""
    print("\n" + "=" * 60)
    print("Available Animation Presets")
    print("=" * 60)

    categories = [
        ('timing', 'Timing Presets'),
        ('render', 'Render Quality'),
        ('color', 'Material Colors'),
        ('fire', 'Fire Intensity'),
        ('camera', 'Camera Settings'),
        ('lighting', 'Lighting Setup')
    ]

    for cat_key, cat_name in categories:
        print(f"\n{cat_name}:")
        print("-" * 60)
        presets = list_presets(cat_key)[cat_key]
        for name, config in presets.items():
            desc = config.get('description', 'No description')
            print(f"  {name:20s} - {desc}")

    print("\n" + "=" * 60)


if __name__ == "__main__":
    # When run directly, print all presets
    print_presets()
