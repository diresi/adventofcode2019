def get_layers(txt, w, h):
    num_layers = len(txt) // (w * h)
    assert w * h * num_layers == len(txt)

    i = 0
    layers = []
    for _ in range(num_layers):
        layer = []
        for _ in range(h):
            layer.append(txt[i:i+w])
            i += w
        layers.append(layer)
    return layers


def count_chars(what, layer):
    return sum(row.count(what) for row in layer)


def get_layer_with_fewest_zeros(layers):
    def key(layer):
        return count_chars("0", layer)
    return sorted(layers, key=key)[0]


def chr_1_times_chr_2(layer):
    return count_chars("1", layer) * count_chars("2", layer)


def img_checksum(txt, w, h):
    layers = get_layers(txt, w, h)
    layer = get_layer_with_fewest_zeros(layers)
    return chr_1_times_chr_2(layer)


def test():
    txt = "123456789012"
    layers = get_layers(txt, 3, 2)
    print(layers)
    assert len(layers) == 2
    assert get_layer_with_fewest_zeros(layers) == layers[0]
    assert chr_1_times_chr_2(layers[0]) == 1
    assert img_checksum(txt, 3, 2) == 1

    assert img_checksum(read_img(), 25, 6) == 1088


def read_img(fn="day8.img"):
    txt = open(fn, encoding="ascii").read()
    return txt.strip()


def main():
    print("day 8/1", img_checksum(read_img(), 25, 6))
    print("day 8/2")

    test()


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Advent of Code 2019")
    args = parser.parse_args()

    main(**vars(args))
