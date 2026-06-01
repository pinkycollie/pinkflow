from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # API
    API_VERSION: str = "v1"
    API_PREFIX: str = "/pinkflow/v1"
    
    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = "/secrets/firebase-credentials.json"
    FIREBASE_PROJECT_ID: str
    
    # DeafAUTH
    DEAFAUTH_PUBLIC_KEY: str
    DEAFAUTH_VERIFY_URL: str = "https://auth.mbtq.dev/validate"
    
    # Fibronrose
    FIBRONROSE_API_KEY: str
    FIBRONROSE_URL: str = "https://api.mbtq.dev/fibronrose"
    
    # PinkSync
    PINKSYNC_API_KEY: str
    PINKSYNC_URL: str = "https://api.mbtq.dev/pinksync"
    
    # Redis
    REDIS_URL: str = "redis://redis:6379"
    
    # Testing
    TEST_DOCKER_SOCKET: str = "/var/run/docker.sock"
    TEST_GPU_ENABLED: bool = True
    
    class Config:
        env_file = ".env"

settings = Settings()
