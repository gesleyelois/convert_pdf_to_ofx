"""
Serviço de categorização inteligente baseado em palavras-chave.
Otimizado para o contexto bancário brasileiro.
"""

import re
from typing import Dict, List, Optional, Tuple
from dataclasses import dataclass
from services.logger import StructuredLogger

@dataclass
class CategoryRule:
    """Regra de categorização com palavras-chave e prioridade."""
    category: str
    keywords: List[str]
    priority: int = 1
    exact_match: bool = False
    case_sensitive: bool = False

class SmartKeywordCategorizer:
    """
    Categorizador inteligente baseado em palavras-chave.
    Usa regras hierárquicas e contexto para melhor categorização.
    """
    
    def __init__(self, logger: StructuredLogger):
        self.logger = logger
        self.categories = self._initialize_categories()
        self._build_regex_patterns()
    
    def _initialize_categories(self) -> List[CategoryRule]:
        """Inicializa as regras de categorização brasileiras."""
        try:
            from keyword_config import CATEGORY_KEYWORDS, CATEGORY_PRIORITIES, TRANSFER_KEYWORDS
        except ImportError:
            # Fallback se o arquivo de configuração não existir
            self.logger.warning("Arquivo keyword_config.py não encontrado. Usando configuração padrão.")
            return self._get_default_categories()
        
        categories = []
        
        # Cria categorias baseadas na configuração
        for category_name, keywords in CATEGORY_KEYWORDS.items():
            priority = CATEGORY_PRIORITIES.get(category_name, 5)
            exact_match = category_name == "Transferências"
            
            categories.append(CategoryRule(
                category=category_name,
                keywords=keywords,
                priority=priority,
                exact_match=exact_match
            ))
        
        # Adiciona categoria "Outros" como fallback
        categories.append(CategoryRule("Outros", [], priority=0))
        
        return categories
    
    def _get_default_categories(self) -> List[CategoryRule]:
        """Retorna categorias padrão caso o arquivo de configuração não exista."""
        return [
            CategoryRule("Alimentação", ["ifood", "rappi", "uber eats", "mcdonalds", "padaria", "restaurante"], priority=10),
            CategoryRule("Transporte", ["uber", "99", "taxi", "combustível", "posto"], priority=10),
            CategoryRule("Saúde", ["farmácia", "drogaria", "hospital", "médico"], priority=9),
            CategoryRule("Moradia", ["aluguel", "condomínio", "energia", "água", "internet"], priority=9),
            CategoryRule("Transferências", ["pix transf", "pix receb", "transferência"], priority=1, exact_match=True),
            CategoryRule("Outros", [], priority=0)
        ]
    
    def _build_regex_patterns(self) -> None:
        """Constrói padrões regex otimizados para cada categoria."""
        for category in self.categories:
            if category.keywords:
                # Cria padrão regex case-insensitive
                pattern = '|'.join(re.escape(keyword) for keyword in category.keywords)
                if not category.case_sensitive:
                    pattern = f'(?i){pattern}'
                category.regex_pattern = re.compile(pattern)
    
    def categorize_transaction(self, description: str, amount: float = 0.0) -> str:
        """
        Categoriza uma transação baseada na descrição.
        
        Args:
            description: Descrição da transação
            amount: Valor da transação (pode influenciar categorização)
            
        Returns:
            Categoria identificada
        """
        if not description:
            return "Outros"
        
        description_clean = self._clean_description(description)
        
        # Busca por correspondências exatas primeiro
        exact_match = self._find_exact_match(description_clean)
        if exact_match:
            return exact_match
        
        # Busca por correspondências de palavras-chave
        best_match = self._find_best_match(description_clean, amount)
        if best_match:
            return best_match
        
        # Aplica regras contextuais
        contextual_match = self._apply_contextual_rules(description_clean, amount)
        if contextual_match:
            return contextual_match
        
        return "Outros"
    
    def _clean_description(self, description: str) -> str:
        """Limpa e normaliza a descrição da transação."""
        # Remove caracteres especiais e normaliza espaços
        cleaned = re.sub(r'[^\w\s]', ' ', description)
        cleaned = re.sub(r'\s+', ' ', cleaned).strip().lower()
        return cleaned
    
    def _find_exact_match(self, description: str) -> Optional[str]:
        """Busca por correspondências exatas."""
        for category in self.categories:
            if category.exact_match:
                for keyword in category.keywords:
                    if keyword.lower() in description:
                        return category.category
        return None
    
    def _find_best_match(self, description: str, amount: float) -> Optional[str]:
        """Encontra a melhor correspondência baseada em palavras-chave."""
        best_category = None
        best_score = 0
        
        for category in self.categories:
            if not category.keywords:
                continue
            
            score = self._calculate_match_score(description, category, amount)
            if score > best_score:
                best_score = score
                best_category = category.category
        
        try:
            from keyword_config import MIN_SCORE_THRESHOLD
        except ImportError:
            MIN_SCORE_THRESHOLD = 0.3
        
        return best_category if best_score > MIN_SCORE_THRESHOLD else None
    
    def _calculate_match_score(self, description: str, category: CategoryRule, amount: float) -> float:
        """Calcula score de correspondência para uma categoria."""
        score = 0
        
        # Verifica correspondências de palavras-chave
        for keyword in category.keywords:
            if keyword.lower() in description:
                # Score baseado na prioridade da categoria
                score += category.priority * 0.1
                
                # Bônus para correspondências mais longas
                if len(keyword) > 3:
                    score += 0.05
        
        # Aplica regras específicas baseadas no valor
        if amount > 0:
            score = self._apply_amount_based_rules(description, category, amount, score)
        
        return score
    
    def _apply_amount_based_rules(self, description: str, category: CategoryRule, amount: float, base_score: float) -> float:
        """Aplica regras baseadas no valor da transação."""
        try:
            from keyword_config import VALUE_BASED_RULES
        except ImportError:
            # Valores padrão se configuração não existir
            VALUE_BASED_RULES = {
                "high_value_threshold": 1000,
                "low_value_threshold": 50,
                "investment_threshold": 5000
            }
        
        score = base_score
        
        # Regras para valores altos
        if amount > VALUE_BASED_RULES["high_value_threshold"]:
            if category.category in ["Investimentos", "Transferências"]:
                score += 0.2
            elif category.category in ["Alimentação", "Transporte"]:
                score -= 0.1
        
        # Regras para valores baixos
        elif amount < VALUE_BASED_RULES["low_value_threshold"]:
            if category.category in ["Alimentação", "Transporte", "Lazer"]:
                score += 0.1
            elif category.category in ["Investimentos", "Transferências"]:
                score -= 0.2
        
        return score
    
    def _apply_contextual_rules(self, description: str, amount: float) -> Optional[str]:
        """Aplica regras contextuais para melhorar categorização."""
        try:
            from keyword_config import VALUE_BASED_RULES, TRANSFER_KEYWORDS
        except ImportError:
            # Valores padrão se configuração não existir
            VALUE_BASED_RULES = {"investment_threshold": 5000}
            TRANSFER_KEYWORDS = ["pix transf", "pix receb", "pix enviado", "transferência"]
        
        # Regras para PIX
        if "pix" in description:
            if "qr" in description:
                return "Transferências"
            elif any(word in description for word in ["receb", "enviado", "transf"]):
                return "Transferências"
        
        # Regras para valores específicos
        if amount > VALUE_BASED_RULES["investment_threshold"]:
            return "Investimentos"
        
        # Regras para padrões de data/hora
        if re.search(r'\d{2}/\d{2}', description):
            # Se tem data, provavelmente é uma transação específica
            pass
        
        return None
    
    def get_category_statistics(self, transactions: List[Tuple[str, float]]) -> Dict[str, int]:
        """Retorna estatísticas de categorização."""
        stats = {}
        for description, amount in transactions:
            category = self.categorize_transaction(description, amount)
            stats[category] = stats.get(category, 0) + 1
        return stats
    
    def add_custom_rule(self, category: str, keywords: List[str], priority: int = 5) -> None:
        """Adiciona regra customizada de categorização."""
        new_rule = CategoryRule(category, keywords, priority)
        self.categories.append(new_rule)
        self._build_regex_patterns()
        self.logger.info(f"Regra customizada adicionada: {category} com {len(keywords)} palavras-chave")
    
    def get_available_categories(self) -> List[str]:
        """Retorna lista de categorias disponíveis."""
        return list(set(rule.category for rule in self.categories)) 