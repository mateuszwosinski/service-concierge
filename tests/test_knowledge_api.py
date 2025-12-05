"""Tests for the Knowledge/Products API."""

from concierge.external_systems import knowledge_api


class TestKnowledgeAPI:
    """Test suite for Knowledge/Products API functionality."""

    def test_search_products_with_results(self) -> None:
        """Test searching for products with results."""
        products = knowledge_api.search_products("merino wool")

        assert len(products) > 0
        # All results should contain "merino" or "wool" somewhere
        for product in products:
            search_text = f"{product.name} {product.description} {' '.join(product.features)}".lower()
            assert "merino" in search_text or "wool" in search_text

    def test_search_products_no_results(self) -> None:
        """Test searching for products with no results."""
        products = knowledge_api.search_products("nonexistent_product_xyz")
        assert len(products) == 0

    def test_search_products_ranking(self) -> None:
        """Test that search results are ranked by relevance."""
        products = knowledge_api.search_products("merino")

        # Should have results
        assert len(products) > 0

        # First result should have "merino" in the name (highest weight)
        assert "merino" in products[0].name.lower()

    def test_get_product_success(self) -> None:
        """Test getting a specific product."""
        product = knowledge_api.get_product("PROD-002")

        assert product is not None
        assert product.product_id == "PROD-002"
        assert product.name == "Merino Wool Henley"
        assert product.price == 185.00
        assert product.category == "Tops"
        assert product.in_stock is True

    def test_get_product_not_found(self) -> None:
        """Test getting non-existent product."""
        product = knowledge_api.get_product("PROD-999")
        assert product is None

    def test_get_products(self) -> None:
        """Test getting all products."""
        products = knowledge_api.get_products()

        assert len(products) > 0
        # Should return both in-stock and out-of-stock products
        assert isinstance(products, list)
        assert all(isinstance(p, type(products[0])) for p in products)

    def test_get_products_by_category(self) -> None:
        """Test getting products by category."""
        products = knowledge_api.get_products_by_category("Outerwear")

        assert len(products) > 0
        assert all(p.category == "Outerwear" for p in products)

    def test_get_products_by_category_case_insensitive(self) -> None:
        """Test that category search is case insensitive."""
        products_lower = knowledge_api.get_products_by_category("outerwear")
        products_upper = knowledge_api.get_products_by_category("OUTERWEAR")

        assert len(products_lower) == len(products_upper)

    def test_get_products_by_category_no_results(self) -> None:
        """Test getting products for category with no products."""
        products = knowledge_api.get_products_by_category("NonExistentCategory")
        assert len(products) == 0

    def test_get_available_products(self) -> None:
        """Test getting all in-stock products."""
        products = knowledge_api.get_available_products()

        assert len(products) > 0
        assert all(p.in_stock is True for p in products)

    def test_get_available_products_excludes_out_of_stock(self) -> None:
        """Test that out-of-stock products are excluded."""
        all_products = knowledge_api.get_products()

        # Count how many are out of stock
        out_of_stock_count = sum(1 for p in all_products if not p.in_stock)

        if out_of_stock_count > 0:
            available = knowledge_api.get_available_products()
            assert len(available) == len(all_products) - out_of_stock_count
            assert len(available) < len(all_products)

    def test_search_policies_with_results(self) -> None:
        """Test searching for policy documents."""
        policies = knowledge_api.search_policies("styling")

        assert len(policies) > 0
        for policy in policies:
            search_text = f"{policy.title} {policy.content} {policy.category} {' '.join(policy.keywords)}".lower()
            assert "styling" in search_text or "style" in search_text

    def test_search_policies_no_results(self) -> None:
        """Test searching for policies with no results."""
        policies = knowledge_api.search_policies("nonexistent_policy_xyz")
        assert len(policies) == 0

    def test_search_policies_ranking(self) -> None:
        """Test that policy search results are ranked by relevance."""
        policies = knowledge_api.search_policies("return")

        assert len(policies) > 0
        # First result should have "return" in title or be highly relevant
        first_policy = policies[0]
        assert (
            "return" in first_policy.title.lower()
            or "return" in first_policy.category.lower()
            or any("return" in kw.lower() for kw in first_policy.keywords)
        )

    def test_get_policy_success(self) -> None:
        """Test getting a specific policy document."""
        policy = knowledge_api.get_policy("POL-004")

        assert policy is not None
        assert policy.doc_id == "POL-004"
        assert "styling" in policy.title.lower() or "styling" in policy.content.lower()

    def test_get_policy_not_found(self) -> None:
        """Test getting non-existent policy."""
        policy = knowledge_api.get_policy("POL-999")
        assert policy is None

    def test_get_policies_by_category(self) -> None:
        """Test getting policies by category."""
        policies = knowledge_api.get_policies_by_category("services")

        assert len(policies) > 0
        assert all(p.category == "services" for p in policies)

    def test_get_policies_by_category_case_insensitive(self) -> None:
        """Test that policy category search is case insensitive."""
        policies_lower = knowledge_api.get_policies_by_category("services")
        policies_upper = knowledge_api.get_policies_by_category("SERVICES")

        assert len(policies_lower) == len(policies_upper)

    def test_get_policies_by_category_no_results(self) -> None:
        """Test getting policies for category with no results."""
        policies = knowledge_api.get_policies_by_category("NonExistentCategory")
        assert len(policies) == 0
