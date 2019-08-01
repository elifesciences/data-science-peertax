from peertax.sentencizer_LDA import custom_sentencizer


class TestCustomSentencizer:
    def test_should_split_simple_sentences(self):
        assert custom_sentencizer([
            'This is the first sentence. This is the second sentence.'
        ]) == [[
            'This is the first sentence.',
            'This is the second sentence.'
        ]]

    def test_should_split_on_question_marks(self):
        assert custom_sentencizer([
            'Is this a sentence? Yes, it is.'
        ]) == [[
            'Is this a sentence?',
            'Yes, it is.'
        ]]

    def test_should_replace_question_marks_inside_parenthesis_with_space(self):
        assert custom_sentencizer([
            'This is a sentence (or is it?).'
        ]) == [[
            'This is a sentence (or is it ).'
        ]]

    def test_should_collapse_consequitive_whitespaces(self):
        assert custom_sentencizer([
            'This       is a sentence.'
        ]) == [[
            'This is a sentence.'
        ]]
