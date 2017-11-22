def calculate_precedence(self):
    # fiat precedence is important to
    if self.precedence:
        return self.precedence

    pairs = self.pairs
    # NOTE: if this fails here then the split character ('_') here is wrong
    # fiats should be quite small, < 10 elements
    fiats = set([self.to_fiat_currency(pair)[0] for pair in pairs])
    fiat_pairings = set()

    for pair in pairs:
        [fiat, currency] = self.to_fiat_currency(pair)

        if fiat in fiats and currency in fiats:
            fiat_pairings.add([fiat, currency])

    precedence = defaultdict(lambda: len(fiats))

    for [fiat, currency] in fiat_pairings:
        precedence[fiat] -=1

    return sorted(precedence, key=lambda (k, v): (v, k)).keys()