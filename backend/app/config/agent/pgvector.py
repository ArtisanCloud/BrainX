from pydantic import BaseModel


class PGVector(BaseModel):
    url: str = "postgresql://user:pass@127.0.0.1:54321/brain_x"
    use_jsonb: bool = True
