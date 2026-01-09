# Dummy Integration for Home Assistant

[![Open your Home Assistant instance and open a repository inside the Home Assistant Community Store.](https://my.home-assistant.io/badges/hacs_repository.svg)](https://my.home-assistant.io/redirect/hacs_repository/?owner=tnomas&repository=HASSTest&category=integration)

A simple Home Assistant custom integration that creates dummy entities for testing and demonstration purposes.

## Features

- **Dummy Temperature Sensor** - Simulates a temperature sensor with random fluctuations (18-28°C)
- **Dummy Light** - A virtual light with on/off and brightness control
- **Dummy Light Switch** - A switch that controls the dummy light state
- **Restart Button** - A button to restart Home Assistant (useful after updates)

The switch and light are linked - toggling one will update the other.

## Installation

### HACS (Recommended)

1. Click the badge above or go to HACS → Integrations → Three dots menu → Custom repositories
2. Add this repository URL and select "Integration" as the category
3. Install "Dummy Integration"
4. Restart Home Assistant

### Manual Installation

1. Copy the `custom_components/dummy_integration` folder to your Home Assistant `config/custom_components/` directory
2. Restart Home Assistant

## Configuration

### UI Setup (Recommended)

1. Go to Settings → Devices & Services
2. Click "+ Add Integration"
3. Search for "Dummy Integration"
4. Click to add

### YAML Setup (Alternative)

Add the following to your `configuration.yaml`:

```yaml
dummy_integration:
```

Restart Home Assistant.

## Entities

The following entities will be created:

| Entity ID | Type | Description |
|-----------|------|-------------|
| `sensor.dummy_temperature` | Sensor | Temperature sensor (°C) |
| `light.dummy_light` | Light | Dimmable light |
| `switch.dummy_light_switch` | Switch | Controls the dummy light |
| `button.restart_home_assistant` | Button | Restart Home Assistant |

## License

MIT
