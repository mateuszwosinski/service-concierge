"""Mock Knowledge and Products API for information retrieval."""

from typing import Optional

from concierge.datatypes.general_types import PolicyDocument, Product


class KnowledgeAPI:
    """Mock API for knowledge base and product information retrieval."""

    def __init__(self) -> None:
        """Initialize the Knowledge API with mock data."""
        self._products: dict[str, Product] = self._initialize_mock_products()
        self._policies: dict[str, PolicyDocument] = self._initialize_mock_policies()

    @staticmethod
    def _initialize_mock_products() -> dict[str, Product]:
        """Create mock product catalog data."""
        return {
            "PROD-001": Product(
                product_id="PROD-001",
                name="Merino Wool Performance Jacket",
                description="Italian merino wool jacket with tailored fit and breathable fabric. Features premium YKK zippers and water-resistant finish. Perfect for urban professionals and outdoor enthusiasts.",
                price=895.00,
                category="Outerwear",
                in_stock=True,
                features=[
                    "100% Italian Merino Wool",
                    "Water-resistant DWR coating",
                    "YKK premium zippers",
                    "Tailored athletic fit",
                    "Interior security pocket",
                ],
            ),
            "PROD-002": Product(
                product_id="PROD-002",
                name="Technical Cashmere Sweater",
                description="Luxury cashmere blend sweater with enhanced durability. Temperature-regulating fabric maintains comfort in all seasons. Modern slim fit with reinforced elbows.",
                price=485.00,
                category="Knitwear",
                in_stock=True,
                features=[
                    "80% Cashmere, 20% Technical Fiber",
                    "Temperature regulating",
                    "Reinforced high-wear areas",
                    "Pilling resistant",
                    "Modern slim fit",
                ],
            ),
            "PROD-003": Product(
                product_id="PROD-003",
                name="Heritage Leather Weekender Bag",
                description="Full-grain Italian leather weekender with brass hardware. Hand-stitched construction and canvas lining. Develops unique patina over time. Limited edition colorway.",
                price=1250.00,
                category="Accessories",
                in_stock=False,
                features=[
                    "Full-grain Italian leather",
                    "Brass hardware",
                    "Hand-stitched seams",
                    "Canvas interior lining",
                    "Develops natural patina",
                ],
            ),
            "PROD-004": Product(
                product_id="PROD-004",
                name="Performance Stretch Trousers",
                description="Japanese technical fabric trousers with four-way stretch and wrinkle resistance. Water-repellent finish with hidden zip pockets. Perfect for travel and active lifestyle.",
                price=395.00,
                category="Bottoms",
                in_stock=True,
                features=[
                    "Japanese technical fabric",
                    "Four-way stretch",
                    "Wrinkle resistant",
                    "Water repellent",
                    "Hidden security pockets",
                ],
            ),
            "PROD-005": Product(
                product_id="PROD-005",
                name="Lightweight Down Vest",
                description="Premium 800-fill goose down vest with ultra-lightweight construction. Packable design fits into its own pocket. Ideal for layering or travel.",
                price=325.00,
                category="Outerwear",
                in_stock=True,
                features=[
                    "800-fill goose down",
                    "Ultra-lightweight ripstop fabric",
                    "Packable into pocket",
                    "DWR water treatment",
                    "Slim athletic fit",
                ],
            ),
            "PROD-006": Product(
                product_id="PROD-006",
                name="Swiss Automatic Watch",
                description="Swiss-made automatic timepiece with sapphire crystal and exhibition caseback. 42mm stainless steel case with Italian leather strap. 100m water resistance.",
                price=2850.00,
                category="Accessories",
                in_stock=True,
                features=[
                    "Swiss automatic movement",
                    "Sapphire crystal",
                    "Exhibition caseback",
                    "Italian leather strap",
                    "100m water resistance",
                ],
            ),
            "PROD-007": Product(
                product_id="PROD-007",
                name="Merino Wool Base Layer Set",
                description="Premium merino wool base layer system. Moisture-wicking and odor-resistant. Flatlock seams prevent chafing. Essential for all-season performance.",
                price=245.00,
                category="Base Layers",
                in_stock=True,
                features=[
                    "New Zealand Merino Wool",
                    "Moisture-wicking",
                    "Naturally odor-resistant",
                    "Flatlock seams",
                    "Temperature regulating",
                ],
            ),
            "PROD-008": Product(
                product_id="PROD-008",
                name="Premium Leather Chelsea Boots",
                description="Handcrafted Italian leather Chelsea boots with Goodyear welt construction. Blake-stitched leather sole and cushioned insole. Modern silhouette with elastic side panels.",
                price=725.00,
                category="Footwear",
                in_stock=True,
                features=[
                    "Italian calfskin leather",
                    "Goodyear welt construction",
                    "Blake-stitched leather sole",
                    "Cushioned leather insole",
                    "Elastic side panels",
                ],
            ),
        }

    @staticmethod
    def _initialize_mock_policies() -> dict[str, PolicyDocument]:
        """Create mock policy and service documents."""
        return {
            "POL-001": PolicyDocument(
                doc_id="POL-001",
                title="Shipping and Delivery",
                content="Complimentary white-glove delivery service on all orders. Standard delivery takes 3-5 business days "
                "with signature required. Express delivery (1-2 business days) available for time-sensitive orders. "
                "International shipping available to over 50 countries with customs handling included. All items are "
                "meticulously packaged in luxury presentation boxes. Track your order with real-time updates via SMS and email.",
                category="shipping",
                keywords=[
                    "shipping",
                    "delivery",
                    "white-glove",
                    "express",
                    "international",
                    "luxury packaging",
                    "tracking",
                ],
            ),
            "POL-002": PolicyDocument(
                doc_id="POL-002",
                title="Returns and Exchanges",
                content="We offer a 60-day return policy for unworn items with original tags attached. Complimentary return "
                "shipping provided for all returns. Items can be exchanged for different sizes or colors at no charge. "
                "Our concierge team will arrange courier pickup at your convenience. Full refund processed within 5 business "
                "days of receiving your return. Personalized or custom-tailored items are final sale.",
                category="returns",
                keywords=["return", "refund", "exchange", "60 days", "complimentary", "concierge", "courier pickup"],
            ),
            "POL-003": PolicyDocument(
                doc_id="POL-003",
                title="Quality Guarantee and Care",
                content="All products are backed by our lifetime quality guarantee covering craftsmanship defects. "
                "Complimentary alterations and repairs available at our atelier for the lifetime of the garment. "
                "Annual professional cleaning service included for leather goods. We stand behind the exceptional "
                "quality of our materials and construction. Our care specialists provide personalized guidance on "
                "maintaining your investment pieces.",
                category="warranty",
                keywords=[
                    "quality",
                    "guarantee",
                    "lifetime",
                    "repair",
                    "alterations",
                    "care",
                    "atelier",
                    "craftsmanship",
                ],
            ),
            "POL-004": PolicyDocument(
                doc_id="POL-004",
                title="Personal Styling Services",
                content="Complimentary personal styling consultation for all clients. Our expert stylists provide wardrobe "
                "assessments, seasonal updates, and complete outfit curation. Book in-person sessions at our showrooms or "
                "virtual consultations from anywhere. Receive personalized lookbooks tailored to your lifestyle and preferences. "
                "Priority access to new collections and exclusive pieces. Styling services include travel wardrobe planning "
                "and special event dressing.",
                category="services",
                keywords=[
                    "styling",
                    "personal stylist",
                    "consultation",
                    "wardrobe",
                    "lookbook",
                    "exclusive",
                    "appointment",
                ],
            ),
            "POL-005": PolicyDocument(
                doc_id="POL-005",
                title="Fitting and Tailoring Services",
                content="Expert fitting appointments available at all our locations. Our master tailors provide precise "
                "measurements and customization recommendations. Complimentary basic alterations on all full-price items. "
                "Custom tailoring services for perfect fit guaranteed. Express alteration service available for time-sensitive "
                "needs. Book appointments online or call our concierge team. Average turnaround for alterations is 7-10 days.",
                category="services",
                keywords=[
                    "fitting",
                    "tailoring",
                    "alterations",
                    "measurements",
                    "custom",
                    "appointment",
                    "perfect fit",
                ],
            ),
            "POL-006": PolicyDocument(
                doc_id="POL-006",
                title="VIP Concierge Program",
                content="Join our VIP program for exclusive benefits and personalized service. Dedicated concierge available "
                "24/7 for styling advice, order assistance, and special requests. Priority access to limited editions and "
                "seasonal previews. Invitations to private shopping events and trunk shows. Complimentary gift wrapping and "
                "monogramming services. Early access to sale events. Annual gift with purchase based on membership tier.",
                category="membership",
                keywords=["VIP", "concierge", "exclusive", "priority", "benefits", "membership", "private events"],
            ),
            "POL-007": PolicyDocument(
                doc_id="POL-007",
                title="Privacy and Security",
                content="We protect your personal information with bank-level encryption. Your data is never shared with "
                "third parties for marketing purposes. Secure payment processing through certified PCI-DSS compliant systems. "
                "All personal styling preferences and measurements are kept strictly confidential. You maintain full control "
                "over your data with options to view, update, or delete at any time. We comply with GDPR, CCPA, and international "
                "privacy regulations.",
                category="privacy",
                keywords=["privacy", "security", "data protection", "encryption", "GDPR", "CCPA", "confidential"],
            ),
        }

    def search_products(self, query: str) -> list[Product]:
        """
        Search products by name, description, category, or features. Use this when clients mention product names or descriptions (e.g., "merino jacket", "leather bag", "winter coats"). This searches across all product fields and returns full product details including product_id. ALWAYS use this function first when clients describe what they're looking for, rather than trying to construct or guess a product_id.

        Args:
            query: Search query string (product name, description, category, or feature keywords)

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

            # Keyword matching for individual words
            query_words = query_lower.split()
            for word in query_words:
                if len(word) > 2:  # Ignore very short words
                    if word in product.name.lower():
                        score += 1.0
                    if word in product.description.lower():
                        score += 0.5

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
