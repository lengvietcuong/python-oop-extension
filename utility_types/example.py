from dataclasses import dataclass
from pprint import pprint
from datetime import date
from utility_types import omit, pick, partial, required


@dataclass
class User:
    id: str
    name: str
    gender: str
    date_of_birth: date
    profile_picture_url: str
    email: str
    phone: str | None = None


# To display profiles on the UI, only the name and profile picture URL are needed.
UserPreview = pick("UserPreview", User, ("name", "profile_picture_url"))

# When updating user profiles, any number of fields can change, except for the ID.
UserUpdate = partial("UserUpdate", omit("", User, ("id")))

# To prevent bots, all fields must be filled out (including the phone number).
UserComplete = required("UserComplete", User)


def main():
    user = User(
        "abc123",
        "John Doe",
        "male",
        date(2000, 1, 1),
        "https://example.com/profile_picture.jpg",
        "john.doe@example.com",
    )
    user_preview = UserPreview(user.name, user.profile_picture_url)
    user_update = UserUpdate(
        profile_picture_url="https://example.com/profile_picture.jpg",
        email="john123@example.com",
    )
    user_complete = UserComplete(
        user.id,
        user.name,
        user.gender,
        user.date_of_birth,
        user.profile_picture_url,
        user.email,
        "1234567890",
    )

    pprint(user)
    pprint(user_preview)
    pprint(user_update)
    pprint(user_complete)


if __name__ == "__main__":
    main()
