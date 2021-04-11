from config import orientation


def main():
    if orientation == "Horizontal":
        import horizontal
        horizontal.horizontal_app()
    else:
        import vertical
        vertical.vertical_app()


if __name__ == "__main__":
    main()
