"""Mock Knowledge and Products API for information retrieval."""

import json
from typing import Optional

from concierge.datatypes.general_types import PolicyDocument, Product
from concierge.paths import POLICIES_DATA_PATH, PRODUCTS_DATA_PATH


class KnowledgeAPI:
    """Mock API for knowledge base and product information retrieval."""

    def __init__(self) -> None:
        """Initialize the Knowledge API with mock data."""
        self._products: dict[str, Product] = self._initialize_mock_products()
        self._policies: dict[str, PolicyDocument] = self._initialize_mock_policies()

    @staticmethod
    def _initialize_mock_products() -> dict[str, Product]:
        """Load mock product catalog data from JSON file."""
        data_path = PRODUCTS_DATA_PATH
        with data_path.open() as f:
            products_data = json.load(f)

        return {product_id: Product(**product_dict) for product_id, product_dict in products_data.items()}

    @staticmethod
    def _initialize_mock_policies() -> dict[str, PolicyDocument]:
        """Load mock policy and service documents from JSON file."""
        data_path = POLICIES_DATA_PATH
        with data_path.open() as f:
            policies_data = json.load(f)

        return {policy_id: PolicyDocument(**policy_dict) for policy_id, policy_dict in policies_data.items()}

    def search_products(self, query: str) -> list[Product]:
        """
        Search products by name, description, category, features, colors, or sizes. Use this when clients mention product names or descriptions (e.g., "merino jacket", "leather bag", "winter coats", "black sweater", "size L"). This searches across all product fields and returns full product details including product_id. ALWAYS use this function first when clients describe what they're looking for, rather than trying to construct or guess a product_id.

        Args:
            query: Search query string (product name, description, category, feature keywords, colors, or sizes)

        Returns:
            List of matching Product objects with complete details (including product_id), sorted by relevance
        """
        query_lower = query.lower()
        results: list[tuple[Product, float]] = []

        for product in self._products.values():
            score = 0.0

            # Check name match (highest weight)
            if query_lower in product.name.lower():
                score += 10.0

            # Check description match
            if query_lower in product.description.lower():
                score += 5.0

            # Check category match
            if query_lower in product.category.lower():
                score += 3.0

            # Check features match
            for feature in product.features:
                if query_lower in feature.lower():
                    score += 2.0

            # Check colors match
            for color in product.colors:
                if query_lower in color.lower():
                    score += 4.0

            # Check sizes match
            for size in product.sizes:
                if query_lower in size.lower() or query_lower == size.lower():
                    score += 3.0

            # Keyword matching for individual words
            query_words = query_lower.split()
            for word in query_words:
                if len(word) > 2:  # Ignore very short words
                    if word in product.name.lower():
                        score += 1.0
                    if word in product.description.lower():
                        score += 0.5
                    # Check if word matches any color
                    for color in product.colors:
                        if word == color.lower():
                            score += 2.0
                    # Check if word matches any size
                    for size in product.sizes:
                        if word == size.lower():
                            score += 1.5

            if score > 0:
                results.append((product, score))

        # Sort by score (highest first)
        results.sort(key=lambda x: x[1], reverse=True)
        return [product for product, _ in results]

    def get_product(self, product_id: str) -> Optional[Product]:
        """
        Get a specific product by its exact product_id. ONLY use this when you already have the exact product_id in format PROD-XXX (e.g., "PROD-001", "PROD-002"). DO NOT use slugified names, product names, or any other format as the product_id. If you need to find a product by name or description, use search_products first to get the correct product_id.

        Args:
            product_id: Exact product identifier in format PROD-XXX (e.g., "PROD-001")

        Returns:
            Product object with full details if found, None otherwise
        """
        return self._products.get(product_id)

    def get_products(self) -> list[Product]:
        """
        Get all products in the catalog.

        Returns:
            List of all Product objects
        """
        return list(self._products.values())

    def get_products_by_category(self, category: str) -> list[Product]:
        """
        Get all products in a category.

        Args:
            category: Product category

        Returns:
            List of Product objects in the category
        """
        category_lower = category.lower()
        return [p for p in self._products.values() if p.category.lower() == category_lower]

    def get_available_products(self) -> list[Product]:
        """
        Get all in-stock products.

        Returns:
            List of Product objects that are in stock
        """
        return [p for p in self._products.values() if p.in_stock]

    def search_policies(self, query: str) -> list[PolicyDocument]:
        """
        Search company policies and information documents. Use this to find information about shipping, returns, warranty, privacy, terms of service, fitting services, styling sessions, VIP programs, and other company policies. Searches across titles, content, and keywords.

        Args:
            query: Search query string (e.g., "shipping", "returns", "warranty", "privacy", "fitting appointment")

        Returns:
            List of matching PolicyDocument objects with full policy details, sorted by relevance
        """
        query_lower = query.lower()
        results: list[tuple[PolicyDocument, float]] = []

        for policy in self._policies.values():
            score = 0.0

            # Check title match (highest weight)
            if query_lower in policy.title.lower():
                score += 10.0

            # Check content match
            if query_lower in policy.content.lower():
                score += 5.0

            # Check keywords match
            for keyword in policy.keywords:
                if query_lower in keyword.lower() or keyword.lower() in query_lower:
                    score += 3.0

            # Check category match
            if query_lower in policy.category.lower():
                score += 2.0

            # Word-by-word matching
            query_words = query_lower.split()
            for word in query_words:
                if len(word) > 2:  # Ignore very short words
                    if word in policy.title.lower():
                        score += 1.0
                    if word in policy.content.lower():
                        score += 0.5
                    for keyword in policy.keywords:
                        if word in keyword.lower():
                            score += 1.0

            if score > 0:
                results.append((policy, score))

        # Sort by score (highest first)
        results.sort(key=lambda x: x[1], reverse=True)
        return [policy for policy, _ in results]

    def get_policy(self, doc_id: str) -> Optional[PolicyDocument]:
        """
        Get a specific policy document by ID.

        Args:
            doc_id: Document identifier

        Returns:
            PolicyDocument if found, None otherwise
        """
        return self._policies.get(doc_id)

    def get_policies_by_category(self, category: str) -> list[PolicyDocument]:
        """
        Get all policy documents in a category.

        Args:
            category: Policy category (shipping, returns, warranty, etc.)

        Returns:
            List of PolicyDocument objects in the category
        """
        category_lower = category.lower()
        return [p for p in self._policies.values() if p.category.lower() == category_lower]


knowledge_api = KnowledgeAPI()
