import aurorax
import pprint


def main():
    # get schema
    schema = aurorax.metadata.get_data_products_schema(3)
    pprint.pprint(schema)


# ----------
if (__name__ == "__main__"):
    main()
