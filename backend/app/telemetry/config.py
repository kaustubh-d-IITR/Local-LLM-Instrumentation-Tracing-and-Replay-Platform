from pydantic_settings import BaseSettings, SettingsConfigDict

class TelemetryConfig(BaseSettings):
    ENABLE_LATENCY: bool = True
    ENABLE_ACTIVATIONS: bool = True
    ENABLE_ANOMALIES: bool = True

    MAX_ACTIVATION_THRESHOLD: float = 50.0
    MAX_LATENCY_THRESHOLD_MS: float = 100.0
    MEMORY_WARNING_THRESHOLD_PERCENT: float = 90.0

    TELEMETRY_SAMPLE_RATE: float = 1.0

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

telemetry_config = TelemetryConfig()
