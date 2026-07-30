from memory.profile_memory import ProfileMemory


class FormFiller:

    def fill(
        self,
        question
    ):

        q = question.lower()

        mapping = {
            "name":
            ProfileMemory.get("name"),

            "email":
            ProfileMemory.get("email"),

            "phone":
            ProfileMemory.get("phone"),

            "experience":
            ProfileMemory.get(
                "experience"
            )
        }

        for key in mapping:

            if key in q:
                return mapping[key]

        return ""