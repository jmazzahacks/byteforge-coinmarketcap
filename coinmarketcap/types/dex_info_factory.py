from typing import Dict
import time
from .dex_info import DexInfo, DexUrls

class DexInfoFactory:
    @staticmethod
    def from_dict(data: Dict) -> DexInfo:
        """
        Create a DexInfo instance from API response dictionary

        Args:
            data: Dictionary containing DEX information from API response

        Returns:
            DexInfo instance
        """
        data = data.copy()

        # Add timestamp if not present
        if 'timestamp' not in data:
            data['timestamp'] = int(time.time())

        # Process URLs if present
        if 'urls' in data and isinstance(data['urls'], dict):
            urls_dict = data.pop('urls')
            data['urls'] = DexUrls(**urls_dict)

        # Remove any fields not in the DexInfo model
        valid_fields = {
            'id', 'name', 'slug', 'logo', 'description',
            'date_launched', 'notice', 'status', 'urls', 'timestamp'
        }

        # Filter out any extra fields from API response
        filtered_data = {k: v for k, v in data.items() if k in valid_fields}

        return DexInfo(**filtered_data)