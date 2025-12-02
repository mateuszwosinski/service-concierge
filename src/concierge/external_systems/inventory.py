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
                name="Wireless Headphones Pro",
                description="Premium wireless headphones with active noise cancellation, 30-hour battery life, and superior sound quality. Perfect for music lovers and professionals.",
                price=199.99,
                category="Audio",
                in_stock=True,
                features=[
                    "Active Noise Cancellation",
                    "30-hour battery life",
                    "Bluetooth 5.0",
                    "Premium sound quality",
                    "Comfortable over-ear design",
                ],
            ),
            "PROD-002": Product(
                product_id="PROD-002",
                name="Ergonomic Keyboard",
                description="Mechanical keyboard with ergonomic split design, reducing wrist strain. RGB backlighting and programmable keys for productivity.",
                price=149.99,
                category="Accessories",
                in_stock=True,
                features=[
                    "Split ergonomic design",
                    "Mechanical switches",
                    "RGB backlighting",
                    "Programmable keys",
                    "Wrist rest included",
                ],
            ),
            "PROD-003": Product(
                product_id="PROD-003",
                name="4K Webcam",
                description="Professional 4K webcam with auto-focus and built-in noise-cancelling microphone. Ideal for video conferencing and streaming.",
                price=129.99,
                category="Video",
                in_stock=False,
                features=[
                    "4K resolution",
                    "Auto-focus",
                    "Noise-cancelling microphone",
                    "Wide-angle lens",
                    "USB-C connection",
                ],
            ),
            "PROD-004": Product(
                product_id="PROD-004",
                name="Standing Desk Converter",
                description="Adjustable standing desk converter that sits on top of your existing desk. Easy height adjustment and spacious work surface.",
                price=249.99,
                category="Furniture",
                in_stock=True,
                features=[
                    "Adjustable height",
                    "Gas spring assist",
                    "Dual-level design",
                    "Sturdy construction",
                    "Easy assembly",
                ],
            ),
            "PROD-005": Product(
                product_id="PROD-005",
                name="USB-C Hub",
                description="Multi-port USB-C hub with HDMI, USB 3.0, SD card reader, and power delivery. Compact and portable design.",
                price=49.99,
                category="Accessories",
                in_stock=True,
                features=[
                    "7-in-1 connectivity",
                    "4K HDMI output",
                    "USB 3.0 ports",
                    "SD/microSD reader",
                    "100W power delivery",
                ],
            ),
            "PROD-006": Product(
                product_id="PROD-006",
                name="Wireless Mouse",
                description="Ergonomic wireless mouse with precision tracking and long battery life. Silent clicks for quiet work environments.",
                price=39.99,
                category="Accessories",
                in_stock=True,
                features=[
                    "Ergonomic design",
                    "Precision tracking",
                    "Silent clicks",
                    "12-month battery",
                    "Wireless 2.4GHz",
                ],
            ),
        }

    @staticmethod
    def _initialize_mock_policies() -> dict[str, PolicyDocument]:
        """Create mock policy and service documents."""
        return {
            "POL-001": PolicyDocument(
                doc_id="POL-001",
                title="Shipping Policy",
                content="We offer free standard shipping on orders over $50 within the continental United States. "
                "Standard shipping takes 5-7 business days. Express shipping (2-3 business days) is available "
                "for $15. International shipping is available to select countries with delivery times of 10-15 "
                "business days. All orders are processed within 1-2 business days.",
                category="shipping",
                keywords=["shipping", "delivery", "free shipping", "express", "international", "processing time"],
            ),
            "POL-002": PolicyDocument(
                doc_id="POL-002",
                title="Return Policy",
                content="We accept returns within 30 days of delivery for most items. Products must be in original "
                "condition with all packaging and accessories. To initiate a return, contact our customer service "
                "team with your order number. Refunds are processed within 5-7 business days after we receive your "
                "return. Return shipping is free for defective items; customers pay return shipping for other returns.",
                category="returns",
                keywords=["return", "refund", "exchange", "30 days", "defective", "customer service"],
            ),
            "POL-003": PolicyDocument(
                doc_id="POL-003",
                title="Warranty Information",
                content="All products come with a 1-year manufacturer warranty covering defects in materials and "
                "workmanship. Extended warranty options are available at checkout. Warranty does not cover damage "
                "from misuse, accidents, or normal wear and tear. To file a warranty claim, contact our support "
                "team with your order number and description of the issue. Warranty repairs or replacements are "
                "provided free of charge.",
                category="warranty",
                keywords=["warranty", "guarantee", "defect", "repair", "replacement", "1 year", "coverage"],
            ),
            "POL-004": PolicyDocument(
                doc_id="POL-004",
                title="Payment Methods",
                content="We accept all major credit cards (Visa, MasterCard, American Express, Discover), PayPal, "
                "Apple Pay, and Google Pay. Payment is processed securely through our encrypted payment gateway. "
                "For orders over $500, additional verification may be required. We do not store credit card "
                "information on our servers. All transactions are PCI-compliant.",
                category="payment",
                keywords=["payment", "credit card", "paypal", "apple pay", "google pay", "secure", "PCI"],
            ),
            "POL-005": PolicyDocument(
                doc_id="POL-005",
                title="Product Support",
                content="Our technical support team is available Monday-Friday, 9am-6pm EST. You can reach us via "
                "email, phone, or live chat. We provide setup assistance, troubleshooting, and product guidance. "
                "Average response time for email inquiries is 24 hours. Phone and chat support offer immediate "
                "assistance. Product manuals and video tutorials are available on our website.",
                category="support",
                keywords=["support", "help", "technical", "troubleshooting", "setup", "contact", "assistance"],
            ),
            "POL-006": PolicyDocument(
                doc_id="POL-006",
                title="Privacy Policy",
                content="We respect your privacy and protect your personal information. We collect only necessary "
                "information for order processing and customer service. Your data is never sold to third parties. "
                "We use industry-standard encryption to protect your information. You can request to view, update, "
                "or delete your personal data at any time. We comply with GDPR and CCPA regulations.",
                category="privacy",
                keywords=["privacy", "data", "personal information", "GDPR", "CCPA", "encryption", "security"],
            ),
        }

    def search_products(self, query: str) -> list[Product]:
        """
        Search products using keyword matching.

        Args:
            query: Search query string

        Returns:
            List of matching Product objects, sorted by relevance
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
        Get a specific product by ID.

        Args:
            product_id: Product identifier

        Returns:
            Product if found, None otherwise
        """
        return self._products.get(product_id)

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
        Search policy documents using keyword matching.

        Args:
            query: Search query string

        Returns:
            List of matching PolicyDocument objects, sorted by relevance
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
