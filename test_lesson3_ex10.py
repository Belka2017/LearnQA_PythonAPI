class Phrase:
    def test_phrase_lenght(self):
        phrase = input("Set a phrase: ")
        max = 15
        assert len(phrase) >= max, f"The length of the phrase is {len(phrase)}. It's more then {max}"