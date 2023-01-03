import flet
from flet import *
import requests
from dotenv import load_dotenv

load_dotenv()

APIKEY = os.getenv("APIKEY")


class AppTitle(UserControl):
    def __init__(self):
        super().__init__()

    def InputContainer(self, width: str, text: str):
        return Container(
            width=width,
            height=40,
            bgcolor="white10",
            border_radius=8,
            padding=8,
            content=Row(
                spacing=10,
                vertical_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Icon(
                        name=icons.SEARCH_ROUNDED,
                        size=17,
                        opacity=0.85,
                    ),
                    TextField(
                        border_color="transparent",
                        height=20,
                        text_size=14,
                        content_padding=0,
                        cursor_color="white",
                        cursor_width=1,
                        color="white",
                        hint_text="Search",
                    ),
                ],
            ),
        )

    def build(self):
        return Container(
            padding=padding.only(top=20, left=15, right=15),
            content=Column(
                horizontal_alignment=CrossAxisAlignment.CENTER,
                controls=[
                    Text(
                        "IMDb Movies & Shows",
                        size=15,
                        weight="bold",
                        text_align="center",
                    ),
                    Divider(height=5, color="transparent"),
                    self.InputContainer(280, "Search"),
                    Divider(height=20, color="white12"),
                ],
            ),
        )


class ComingSoon(UserControl):
    def __init__(self):
        super().__init__()

    def ComingSoonTitle(self):
        res = requests.get("https://imdb-api.com/en/API/ComingSoon/" + APIKEY)
        self.movie_list = GridView(
            expand=True,
            child_aspect_ratio=1.65,
            horizontal=True,
        )

        for movie in range(len(res.json()["items"]) - 112):
            self.movie_list.controls.append(
                Column(
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Container(
                            expand=9,
                            border_radius=12,
                            bgcolor="white10",
                            image_fit=ImageFit.FILL,
                            image_src=res.json()["items"][movie]["image"],
                        ),
                        Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            expand=2,
                            spacing=2,
                            controls=[
                                Text(
                                    res.json()["items"][movie]["title"],
                                    size=11,
                                    no_wrap=True,
                                ),
                                Text(
                                    res.json()["items"][movie]["releaseState"],
                                    size=10,
                                    color="white54",
                                ),
                            ],
                        ),
                    ],
                ),
            )

        return self.movie_list

    def build(self):
        return Container(
            width=280,
            height=240,
            content=Column(
                controls=[
                    Row(
                        controls=[
                            Text(
                                "Coming Soon",
                                size=14,
                            ),
                        ]
                    ),
                    self.ComingSoonTitle(),
                ]
            ),
        )


class TopTvShows(UserControl):
    def __init__(self):
        super().__init__()

    def TrendingTVShows(self):
        res = requests.get("https://imdb-api.com/API/MostPopularTVs/" + APIKEY)

        self.tv_list = GridView(
            child_aspect_ratio=1.2,
            expand=True,
            horizontal=True,
            spacing=25,
        )

        for show in range(len(res.json()["items"]) - 80):
            self.tv_list.controls.append(
                Column(
                    horizontal_alignment=CrossAxisAlignment.CENTER,
                    controls=[
                        Container(
                            expand=9,
                            border_radius=10,
                            image_fit=ImageFit.FILL,
                            image_src=res.json()["items"][show]["image"],
                            on_hover=lambda e: self.GetVideo(e),
                        ),
                        Column(
                            horizontal_alignment=CrossAxisAlignment.CENTER,
                            expand=2,
                            spacing=2,
                            controls=[
                                Row(
                                    alignment=MainAxisAlignment.SPACE_BETWEEN,
                                    spacing=0,
                                    controls=[
                                        Text(
                                            res.json()["items"][show]["title"], size=11
                                        ),
                                        Text(
                                            res.json()["items"][show]["year"],
                                            size=10,
                                            color="white54",
                                        ),
                                    ],
                                ),
                                Row(
                                    alignment=MainAxisAlignment.START,
                                    spacing=2,
                                    controls=[
                                        Icon(
                                            icons.STAR_RATE_ROUNDED,
                                            size=13,
                                            color="yellow600",
                                        ),
                                        Text(
                                            res.json()["items"][show]["imDbRating"],
                                            size=11,
                                            color="white54",
                                        ),
                                    ],
                                ),
                            ],
                        ),
                    ],
                ),
            )
        return self.tv_list

    def build(self):
        return Container(
            width=280,
            height=240,
            clip_behavior=ClipBehavior.HARD_EDGE,
            content=Column(
                controls=[
                    Row(
                        controls=[
                            Text(
                                "Trending TV Shows",
                                size=14,
                            ),
                        ]
                    ),
                    self.TrendingTVShows(),
                ],
            ),
        )


def main(page: Page):
    page.title = "Flet UI With IMDb API"
    page.horizontal_alignment = CrossAxisAlignment.CENTER
    page.vertical_alignment = MainAxisAlignment.CENTER
    page.bgcolor = "white"

    _main_ = Container(
        width=280,
        height=600,
        border=border.all(1, "black"),
        padding=10,
        clip_behavior=ClipBehavior.HARD_EDGE,
        content=Column(
            scroll="none",
            horizontal_alignment=CrossAxisAlignment.CENTER,
            controls=[
                AppTitle(),
                Container(
                    expand=True,
                    padding=10,
                    content=Column(
                        scroll="hidden",
                        controls=[
                            ComingSoon(),
                            Divider(height=10, color="white10"),
                            TopTvShows(),
                            Container(),
                        ],
                    ),
                ),
            ],
        ),
        gradient=RadialGradient(
            center=Alignment(-0.5, -0.8),
            radius=3,
            colors=[
                # "#42445f",
                # "#393b52",
                "#33354a",
                "#2f3143",
                "#2f3143",
                "#292b3c",
                "#222331",
                "#222331",
                "#1a1a25",
                "#1a1b26",
                "#1a1b26",
                "#21222f",
                "#1d1e2a",
                "black",
            ],
        ),
        border_radius=30,
    )
    page.add(_main_)
    page.update()


if __name__ == "__main__":
    flet.app(target=main)
