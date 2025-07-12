"""
Configurações centralizadas do projeto.
Seguindo o princípio de Single Responsibility e evitando magic numbers.
"""

import os
from pathlib import Path

# Diretórios
BASE_DIR = Path(__file__).parent
PDFS_DIR = BASE_DIR / 'pdfs'
OFXS_DIR = BASE_DIR / 'ofxs_gerados'
OFXS_CATEGORIZADOS_DIR = BASE_DIR / 'ofxs_categorizados'
TEMP_DIR = BASE_DIR / 'temp'

# Configurações de bancos
BANK_CONFIGS = {
    'itau': {
        'name': 'Itaú',
        'agency': '7431',
        'account': '052607-3',
        'bank_id': '0260',
        'org': 'ITAÚ UNIBANCO S.A.',
        'fid': '260'
    },
    'mercadopago': {
        'name': 'Mercado Pago',
        'agency': '1',
        'account': '74645773646',
        'bank_id': '323',
        'org': 'MERCADO PAGO INSTITUIÇÃO DE PAGAMENTO LTDA.',
        'fid': '323'
    }
}

# Configurações OFX
OFX_CONFIG = {
    'version': '102',
    'security': 'NONE',
    'encoding': 'UTF-8',
    'charset': 'NONE',
    'compression': 'NONE',
    'language': 'POR',
    'currency': 'BRL',
    'account_type': 'CHECKING',
    'timezone': '[-3:BRT]',
    'gmt_timezone': '[0:GMT]'
}

# Configurações de logging
LOG_CONFIG = {
    'level': 'INFO',
    'format': '[%(levelname)s] %(message)s',
    'date_format': '%Y-%m-%d %H:%M:%S'
}

# Configurações de processamento
PROCESSING_CONFIG = {
    'max_file_size_mb': 50,
    'supported_extensions': ['.pdf'],
    'temp_cleanup_enabled': True
} 