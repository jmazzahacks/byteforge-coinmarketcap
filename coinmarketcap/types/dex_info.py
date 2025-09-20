from dataclasses import dataclass
from typing import Optional, Dict, List

@dataclass
class DexUrls:
    """URLs associated with a DEX"""
    website: Optional[List[str]] = None
    twitter: Optional[List[str]] = None
    blog: Optional[List[str]] = None
    chat: Optional[List[str]] = None
    fee: Optional[List[str]] = None

    def __post_init__(self):
        """Post-initialization processing"""
        self.website = self.website or []
        self.twitter = self.twitter or []
        self.blog = self.blog or []
        self.chat = self.chat or []
        self.fee = self.fee or []

@dataclass
class DexInfo:
    """Data model for DEX (Decentralized Exchange) information"""

    id: int
    name: str
    slug: str
    logo: Optional[str] = None
    description: Optional[str] = None
    date_launched: Optional[str] = None
    notice: Optional[str] = None
    status: Optional[str] = None
    urls: Optional[DexUrls] = None
    timestamp: Optional[int] = None

    def __post_init__(self):
        """Post-initialization processing"""
        if self.urls is None:
            self.urls = DexUrls()