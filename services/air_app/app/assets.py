"""bundles and minifies css and js for each blueprint"""
from flask import current_app as app
from flask_assets import Bundle


def compile_assets(assets):
    """bundles and minifies css and js for each blueprint"""
    assets.auto_build = True
    assets.debug = False
    main_style_bundle = Bundle(
        "src/css/*.css",
        filters="cssmin",
        output="dist/css/style.css",
        extra={"rel": "stylesheet/css"},
    )
    main_js_bundle = Bundle("src/js/*.js", filters="jsmin", output="dist/js/main.min.js")

    home_style_bundle = Bundle(
        "src/css/*.css",
        "home_bp/home.css",
        filters="cssmin",
        output="dist/css/home.css",
        extra={"rel": "stylesheet/css"},
    )

    home_js_bundle = Bundle("home_bp/home.js", filters="jsmin", output="dist/js/home.min.js")

    auth_style_bundle = Bundle(
        "src/css/*.css",
        "auth_bp/auth.css",
        filters="cssmin",
        output="dist/css/auth.css",
        extra={"rel": "stylesheet/css"},
    )

    assets.register("main_style_bundle", main_style_bundle)
    assets.register("main_js_bundle", main_js_bundle)
    assets.register("home_style_bundle", home_style_bundle)
    assets.register("home_js_bundle", home_js_bundle)
    assets.register("auth_styles_bundle", auth_style_bundle)
    if app.config["FLASK_DEBUG"] == "true":
        main_style_bundle.build()
        main_js_bundle.build()
        home_style_bundle.build()
        home_js_bundle.build()
        auth_style_bundle.build()
    return assets
