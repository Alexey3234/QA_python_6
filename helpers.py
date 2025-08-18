def generate_phone_number():
    from random import randint
    return f"8{randint(1000000000, 9999999999)}"

def generate_random_string(length=10):
    import random
    import string
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))


from pages.main_page import MainPage

class QuestionHelpers:
    @staticmethod
    def verify_all_answers_collapsed(main_page: MainPage) -> bool:
        return (not main_page.is_answer_visible(0) and
                not main_page.is_answer_visible(1) and
                not main_page.is_answer_visible(2) and
                not main_page.is_answer_visible(3) and
                not main_page.is_answer_visible(4) and
                not main_page.is_answer_visible(5) and
                not main_page.is_answer_visible(6) and
                not main_page.is_answer_visible(7))

    @staticmethod
    def verify_only_one_answer_visible(main_page: MainPage, visible_index: int) -> bool:
        checks = [
            main_page.is_answer_visible(0),
            main_page.is_answer_visible(1),
            main_page.is_answer_visible(2),
            main_page.is_answer_visible(3),
            main_page.is_answer_visible(4),
            main_page.is_answer_visible(5),
            main_page.is_answer_visible(6),
            main_page.is_answer_visible(7)
        ]
        
        return (checks[visible_index] and
                not checks[(visible_index + 1) % 8] and
                not checks[(visible_index + 2) % 8] and
                not checks[(visible_index + 3) % 8] and
                not checks[(visible_index + 4) % 8] and
                not checks[(visible_index + 5) % 8] and
                not checks[(visible_index + 6) % 8] and
                not checks[(visible_index + 7) % 8])