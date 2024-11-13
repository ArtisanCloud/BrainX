def print_routes(app):
    # 在添加路由后
    print("\nRegistered Routes:")
    print("-" * 80)
    print(f"{'Method':<20} {'Path':<60}")
    print("-" * 80)
    for route in app.routes:
        methods = route.methods if hasattr(route, 'methods') else set()
        methods_str = ", ".join(sorted(methods)) if methods else "No methods"
        print(f"{methods_str:<20} {route.path:<60}")