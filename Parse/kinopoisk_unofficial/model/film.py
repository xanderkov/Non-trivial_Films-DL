from dataclasses import dataclass
from typing import List, Optional, Union

from kinopoisk_unofficial.model.country import Country
from kinopoisk_unofficial.model.dictonary.film_type import FilmType
from kinopoisk_unofficial.model.dictonary.production_status import ProductionStatus
from kinopoisk_unofficial.model.genre import Genre


@dataclass
class Film:
    kinopoisk_id: int = None
    imdb_id: Optional[str] = None
    name_ru: str = None
    coverUrl: Optional[str] = None
    name_en: Optional[Union[str, None]] = None
    name_original: Optional[str] = None
    poster_url: Optional[str] = None
    poster_url_preview: Optional[str] = None
    reviews_count: Optional[int] = None
    rating_good_review: Optional[float] = None
    rating_good_review_vote_count: Optional[int] = None
    rating_kinopoisk: Optional[float] = None
    rating_kinopoisk_vote_count: Optional[int] = None
    rating_imdb: Optional[float] = None
    rating_imdb_vote_count: Optional[int] = None
    rating_film_critics: Optional[float] = None
    rating_film_critics_vote_count: Optional[int] = None
    rating_await: Optional[Union[float, None]] = None
    rating_await_count: Optional[int] = None
    rating_rf_critics: Optional[Union[float, None]] = None
    rating_rf_critics_vote_count: Optional[int] = None
    year: Optional[int] = None
    film_length: Optional[int] = None
    is_tickets_available: Optional[bool] = None
    production_status: Optional[Union[ProductionStatus, None]] = None
    type: Optional[FilmType] = None
    has_imax: Optional[bool] = None
    has_3_d: Optional[bool] = None
    countries: Optional[List[Country]] = None
    genres: Optional[List[Genre]] = None
    start_year: Optional[Union[int, None]] = None
    end_year: Optional[Union[int, None]] = None
    web_url: Optional[str] = None
    slogan: Optional[str] = None
    description: str = None
    short_description: Optional[str] = None
    editor_annotation: Optional[str] = None
    rating_mpaa: Optional[str] = None
    rating_age_limits: Optional[str] = None
    last_sync: Optional[str] = None
    serial: Optional[bool] = None
    short_film: Optional[bool] = None
    completed: Optional[bool] = None