# pylint: disable=too-many-lines
from __future__ import annotations

from typing import TYPE_CHECKING, List, Optional, Union, overload

if TYPE_CHECKING:
    from .tailwind_types.accent_color import AccentColor
    from .tailwind_types.align_content import AlignContent
    from .tailwind_types.align_items import AlignItems
    from .tailwind_types.align_self import AlignSelf
    from .tailwind_types.animation import Animation
    from .tailwind_types.appearance import Appearance
    from .tailwind_types.aspect_ratio import AspectRatio
    from .tailwind_types.backdrop_blur import BackdropBlur
    from .tailwind_types.backdrop_brightness import BackdropBrightness
    from .tailwind_types.backdrop_contrast import BackdropContrast
    from .tailwind_types.backdrop_grayscale import BackdropGrayscale
    from .tailwind_types.backdrop_hue_rotate import BackdropHueRotate
    from .tailwind_types.backdrop_invert import BackdropInvert
    from .tailwind_types.backdrop_opacity import BackdropOpacity
    from .tailwind_types.backdrop_saturate import BackdropSaturate
    from .tailwind_types.backdrop_sepia import BackdropSepia
    from .tailwind_types.background_attachment import BackgroundAttachment
    from .tailwind_types.background_blend_mode import BackgroundBlendMode
    from .tailwind_types.background_clip import BackgroundClip
    from .tailwind_types.background_color import BackgroundColor
    from .tailwind_types.background_image import BackgroundImage
    from .tailwind_types.background_origin import BackgroundOrigin
    from .tailwind_types.background_position import BackgroundPosition
    from .tailwind_types.background_repeat import BackgroundRepeat
    from .tailwind_types.background_size import BackgroundSize
    from .tailwind_types.blur import Blur
    from .tailwind_types.border_collapse import BorderCollapse
    from .tailwind_types.border_color import BorderColor
    from .tailwind_types.border_radius import BorderRadius
    from .tailwind_types.border_spacing import BorderSpacing
    from .tailwind_types.border_style import BorderStyle
    from .tailwind_types.border_width import BorderWidth
    from .tailwind_types.box_decoration_break import BoxDecorationBreak
    from .tailwind_types.box_shadow import BoxShadow
    from .tailwind_types.box_shadow_color import BoxShadowColor
    from .tailwind_types.box_sizing import BoxSizing
    from .tailwind_types.break_after import BreakAfter
    from .tailwind_types.break_before import BreakBefore
    from .tailwind_types.break_inside import BreakInside
    from .tailwind_types.brightness import Brightness
    from .tailwind_types.caption_side import CaptionSide
    from .tailwind_types.caret_color import CaretColor
    from .tailwind_types.clear import Clear
    from .tailwind_types.columns import Columns
    from .tailwind_types.content import Content
    from .tailwind_types.contrast import Contrast
    from .tailwind_types.cursor import Cursor
    from .tailwind_types.display import Display
    from .tailwind_types.divide_color import DivideColor
    from .tailwind_types.divide_style import DivideStyle
    from .tailwind_types.divide_width import DivideWidth
    from .tailwind_types.drop_shadow import DropShadow
    from .tailwind_types.fill import Fill
    from .tailwind_types.flex import Flex
    from .tailwind_types.flex_basis import FlexBasis
    from .tailwind_types.flex_direction import FlexDirection
    from .tailwind_types.flex_grow import FlexGrow
    from .tailwind_types.flex_shrink import FlexShrink
    from .tailwind_types.flex_wrap import FlexWrap
    from .tailwind_types.floats import Floats
    from .tailwind_types.font_family import FontFamily
    from .tailwind_types.font_size import FontSize
    from .tailwind_types.font_smoothing import FontSmoothing
    from .tailwind_types.font_style import FontStyle
    from .tailwind_types.font_variant_numeric import FontVariantNumeric
    from .tailwind_types.font_weight import FontWeight
    from .tailwind_types.gap import Gap
    from .tailwind_types.gradient_color_stops import GradientColorStops
    from .tailwind_types.grayscale import Grayscale
    from .tailwind_types.grid_auto_columns import GridAutoColumns
    from .tailwind_types.grid_auto_flow import GridAutoFlow
    from .tailwind_types.grid_auto_rows import GridAutoRows
    from .tailwind_types.grid_column_start_end import GridColumnStartEnd
    from .tailwind_types.grid_row_start_end import GridRowStartEnd
    from .tailwind_types.grid_template_columns import GridTemplateColumns
    from .tailwind_types.grid_template_rows import GridTemplateRows
    from .tailwind_types.height import Height
    from .tailwind_types.hue_rotate import HueRotate
    from .tailwind_types.hyphens import Hyphens
    from .tailwind_types.invert import Invert
    from .tailwind_types.isolation import Isolation
    from .tailwind_types.justify_content import JustifyContent
    from .tailwind_types.justify_items import JustifyItems
    from .tailwind_types.justify_self import JustifySelf
    from .tailwind_types.letter_spacing import LetterSpacing
    from .tailwind_types.line_clamp import LineClamp
    from .tailwind_types.line_height import LineHeight
    from .tailwind_types.list_style_image import ListStyleImage
    from .tailwind_types.list_style_position import ListStylePosition
    from .tailwind_types.list_style_type import ListStyleType
    from .tailwind_types.margin import Margin
    from .tailwind_types.max_height import MaxHeight
    from .tailwind_types.max_width import MaxWidth
    from .tailwind_types.min_height import MinHeight
    from .tailwind_types.min_width import MinWidth
    from .tailwind_types.mix_blend_mode import MixBlendMode
    from .tailwind_types.object_fit import ObjectFit
    from .tailwind_types.object_position import ObjectPosition
    from .tailwind_types.opacity import Opacity
    from .tailwind_types.order import Order
    from .tailwind_types.outline_color import OutlineColor
    from .tailwind_types.outline_offset import OutlineOffset
    from .tailwind_types.outline_style import OutlineStyle
    from .tailwind_types.outline_width import OutlineWidth
    from .tailwind_types.overflow import Overflow
    from .tailwind_types.overscroll_behavior import OverscrollBehavior
    from .tailwind_types.padding import Padding
    from .tailwind_types.place_content import PlaceContent
    from .tailwind_types.place_items import PlaceItems
    from .tailwind_types.place_self import PlaceSelf
    from .tailwind_types.pointer_events import PointerEvents
    from .tailwind_types.position import Position
    from .tailwind_types.resize import Resize
    from .tailwind_types.ring_color import RingColor
    from .tailwind_types.ring_offset_color import RingOffsetColor
    from .tailwind_types.ring_offset_width import RingOffsetWidth
    from .tailwind_types.ring_width import RingWidth
    from .tailwind_types.rotate import Rotate
    from .tailwind_types.saturate import Saturate
    from .tailwind_types.scale import Scale
    from .tailwind_types.screen_readers import ScreenReaders
    from .tailwind_types.scroll_behavior import ScrollBehavior
    from .tailwind_types.scroll_margin import ScrollMargin
    from .tailwind_types.scroll_padding import ScrollPadding
    from .tailwind_types.scroll_snap_align import ScrollSnapAlign
    from .tailwind_types.scroll_snap_stop import ScrollSnapStop
    from .tailwind_types.scroll_snap_type import ScrollSnapType
    from .tailwind_types.sepia import Sepia
    from .tailwind_types.skew import Skew
    from .tailwind_types.space_between import SpaceBetween
    from .tailwind_types.stroke import Stroke
    from .tailwind_types.stroke_width import StrokeWidth
    from .tailwind_types.table_layout import TableLayout
    from .tailwind_types.text_align import TextAlign
    from .tailwind_types.text_color import TextColor
    from .tailwind_types.text_decoration import TextDecoration
    from .tailwind_types.text_decoration_color import TextDecorationColor
    from .tailwind_types.text_decoration_style import TextDecorationStyle
    from .tailwind_types.text_decoration_thickness import TextDecorationThickness
    from .tailwind_types.text_indent import TextIndent
    from .tailwind_types.text_overflow import TextOverflow
    from .tailwind_types.text_transform import TextTransform
    from .tailwind_types.text_underline_offset import TextUnderlineOffset
    from .tailwind_types.top_right_bottom_left import TopRightBottomLeft
    from .tailwind_types.touch_action import TouchAction
    from .tailwind_types.transform_origin import TransformOrigin
    from .tailwind_types.transition_delay import TransitionDelay
    from .tailwind_types.transition_duration import TransitionDuration
    from .tailwind_types.transition_property import TransitionProperty
    from .tailwind_types.transition_timing_function import TransitionTimingFunction
    from .tailwind_types.translate import Translate
    from .tailwind_types.user_select import UserSelect
    from .tailwind_types.vertical_align import VerticalAlign
    from .tailwind_types.visibility import Visibility
    from .tailwind_types.whitespace import Whitespace
    from .tailwind_types.width import Width
    from .tailwind_types.will_change import WillChange
    from .tailwind_types.word_break import WordBreak
    from .tailwind_types.z_index import ZIndex


class PseudoElement:

    def __init__(self) -> None:
        self._classes: List[str] = []

    def classes(self, add: str) -> None:
        """Add the given classes to the element."""
        self._classes.append(add)


class Tailwind:

    def __init__(self):
        pass

    def aspect_ratio(self, value: AspectRatio) -> Tailwind:
        """Utilities for controlling the aspect ratio of an element."""
        data = 'aspect-' + value
        return data

    def container(self) -> Tailwind:
        """A component for fixing an element's width to the current breakpoint."""
        data = 'container'
        return data

    def columns(self, value: Columns) -> Tailwind:
        """Utilities for controlling the number of columns within an element."""
        data = 'columns-' + value
        return data

    def break_after(self, value: BreakAfter) -> Tailwind:
        """Utilities for controlling how a column or page should break after an element."""
        data = 'break-after-' + value
        return data

    def break_before(self, value: BreakBefore) -> Tailwind:
        """Utilities for controlling how a column or page should break before an element."""
        data = 'break-before-' + value
        return data

    def break_inside(self, value: BreakInside) -> Tailwind:
        """Utilities for controlling how a column or page should break within an element."""
        data = 'break-inside-' + value
        return data

    def box_decoration_break(self, value: BoxDecorationBreak) -> Tailwind:
        """Utilities for controlling how element fragments should be rendered across multiple lines, columns, or pages."""
        data = 'box-decoration-' + value
        return data

    def box_sizing(self, value: BoxSizing) -> Tailwind:
        """Utilities for controlling how the browser should calculate an element's total size."""
        data = 'box-' + value
        return data

    def display(self, value: Display) -> Tailwind:
        """Utilities for controlling the display box type of an element."""
        data = '' + value
        return data

    def floats(self, value: Floats) -> Tailwind:
        """Utilities for controlling the wrapping of content around an element."""
        data = 'float-' + value
        return data

    def clear(self, value: Clear) -> Tailwind:
        """Utilities for controlling the wrapping of content around an element."""
        data = 'clear-' + value
        return data

    def isolation(self, value: Isolation) -> Tailwind:
        """Utilities for controlling whether an element should explicitly create a new stacking context."""
        data = '' + value
        return data

    def object_fit(self, value: ObjectFit) -> Tailwind:
        """Utilities for controlling how a replaced element's content should be resized."""
        data = 'object-' + value
        return data

    def object_position(self, value: ObjectPosition) -> Tailwind:
        """Utilities for controlling how a replaced element's content should be positioned within its container."""
        data = 'object-' + value
        return data

    def overflow(self, value: Overflow) -> Tailwind:
        """Utilities for controlling how an element handles content that is too large for the container."""
        data = 'overflow-' + value
        return data

    def overscroll_behavior(self, value: OverscrollBehavior) -> Tailwind:
        """Utilities for controlling how the browser behaves when reaching the boundary of a scrolling area."""
        data = 'overscroll-' + value
        return data

    def position(self, value: Position) -> Tailwind:
        """Utilities for controlling how an element is positioned in the DOM."""
        data = '' + value
        return data

    def top_right_bottom_left(self, value: TopRightBottomLeft) -> Tailwind:
        """Utilities for controlling the placement of positioned elements."""
        data = '' + value
        return data

    def visibility(self, value: Visibility) -> Tailwind:
        """Utilities for controlling the visibility of an element."""
        data = '' + value
        return data

    def z_index(self, value: ZIndex) -> Tailwind:
        """Utilities for controlling the stack order of an element."""
        data = 'z-' + value
        return data

    def flex_basis(self, value: FlexBasis) -> Tailwind:
        """Utilities for controlling the initial size of flex items."""
        data = 'basis-' + value
        return data

    def flex_direction(self, value: FlexDirection) -> Tailwind:
        """Utilities for controlling the direction of flex items."""
        data = 'flex-' + value
        return data

    def flex_wrap(self, value: FlexWrap) -> Tailwind:
        """Utilities for controlling how flex items wrap."""
        data = 'flex-' + value
        return data

    def flex(self, value: Flex) -> Tailwind:
        """Utilities for controlling how flex items both grow and shrink."""
        data = 'flex-' + value
        return data

    def flex_grow(self, value: FlexGrow) -> Tailwind:
        """Utilities for controlling how flex items grow."""
        data = 'grow-' + value if value else 'grow'
        return data

    def flex_shrink(self, value: FlexShrink) -> Tailwind:
        """Utilities for controlling how flex items shrink."""
        data = 'shrink-' + value if value else 'shrink'
        return data

    def order(self, value: Order) -> Tailwind:
        """Utilities for controlling the order of flex and grid items."""
        data = 'order-' + value
        return data

    def grid_template_columns(self, value: GridTemplateColumns) -> Tailwind:
        """Utilities for specifying the columns in a grid layout."""
        data = 'grid-cols-' + value
        return data

    def grid_column_start_end(self, value: GridColumnStartEnd) -> Tailwind:
        """Utilities for controlling how elements are sized and placed across grid columns."""
        data = 'col-' + value
        return data

    def grid_template_rows(self, value: GridTemplateRows) -> Tailwind:
        """Utilities for specifying the rows in a grid layout."""
        data = 'grid-rows-' + value
        return data

    def grid_row_start_end(self, value: GridRowStartEnd) -> Tailwind:
        """Utilities for controlling how elements are sized and placed across grid rows."""
        data = 'row-' + value
        return data

    def grid_auto_flow(self, value: GridAutoFlow) -> Tailwind:
        """Utilities for controlling how elements in a grid are auto-placed."""
        data = 'grid-flow-' + value
        return data

    def grid_auto_columns(self, value: GridAutoColumns) -> Tailwind:
        """Utilities for controlling the size of implicitly-created grid columns."""
        data = 'auto-cols-' + value
        return data

    def grid_auto_rows(self, value: GridAutoRows) -> Tailwind:
        """Utilities for controlling the size of implicitly-created grid rows."""
        data = 'auto-rows-' + value
        return data

    def gap(self, value: Gap) -> Tailwind:
        """Utilities for controlling gutters between grid and flexbox items."""
        data = 'gap-' + value
        return data

    def justify_content(self, value: JustifyContent) -> Tailwind:
        """Utilities for controlling how flex and grid items are positioned along a container's main axis."""
        data = 'justify-' + value
        return data

    def justify_items(self, value: JustifyItems) -> Tailwind:
        """Utilities for controlling how grid items are aligned along their inline axis."""
        data = 'justify-items-' + value
        return data

    def justify_self(self, value: JustifySelf) -> Tailwind:
        """Utilities for controlling how an individual grid item is aligned along its inline axis."""
        data = 'justify-self-' + value
        return data

    def align_content(self, value: AlignContent) -> Tailwind:
        """Utilities for controlling how rows are positioned in multi-row flex and grid containers."""
        data = 'content-' + value
        return data

    def align_items(self, value: AlignItems) -> Tailwind:
        """Utilities for controlling how flex and grid items are positioned along a container's cross axis."""
        data = 'items-' + value
        return data

    def align_self(self, value: AlignSelf) -> Tailwind:
        """Utilities for controlling how an individual flex or grid item is positioned along its container's cross axis."""
        data = 'self-' + value
        return data

    def place_content(self, value: PlaceContent) -> Tailwind:
        """Utilities for controlling how content is justified and aligned at the same time."""
        data = 'place-content-' + value
        return data

    def place_items(self, value: PlaceItems) -> Tailwind:
        """Utilities for controlling how items are justified and aligned at the same time."""
        data = 'place-items-' + value
        return data

    def place_self(self, value: PlaceSelf) -> Tailwind:
        """Utilities for controlling how an individual item is justified and aligned at the same time."""
        data = 'place-self-' + value
        return data

    def padding(self, value: Padding) -> Tailwind:
        """Utilities for controlling an element's padding."""
        data = '' + value
        return data

    def margin(self, value: Margin) -> Tailwind:
        """Utilities for controlling an element's margin."""
        data = '' + value
        return data

    def space_between(self, value: SpaceBetween) -> Tailwind:
        """Utilities for controlling the space between child elements."""
        data = 'space-' + value
        return data

    def width(self, value: Width) -> Tailwind:
        """Utilities for setting the width of an element."""
        data = 'w-' + value
        return data

    def min_width(self, value: MinWidth) -> Tailwind:
        """Utilities for setting the minimum width of an element."""
        data = 'min-w-' + value
        return data

    def max_width(self, value: MaxWidth) -> Tailwind:
        """Utilities for setting the maximum width of an element."""
        data = 'max-w-' + value
        return data

    def height(self, value: Height) -> Tailwind:
        """Utilities for setting the height of an element."""
        data = 'h-' + value
        return data

    def min_height(self, value: MinHeight) -> Tailwind:
        """Utilities for setting the minimum height of an element."""
        data = 'min-h-' + value
        return data

    def max_height(self, value: MaxHeight) -> Tailwind:
        """Utilities for setting the maximum height of an element."""
        data = 'max-h-' + value
        return data

    def font_family(self, value: FontFamily) -> Tailwind:
        """Utilities for controlling the font family of an element."""
        data = 'font-' + value
        return data

    def font_size(self, value: FontSize) -> Tailwind:
        """Utilities for controlling the font size of an element."""
        data = 'text-' + value
        return data

    def font_smoothing(self, value: FontSmoothing) -> Tailwind:
        """Utilities for controlling the font smoothing of an element."""
        data = '' + value
        return data

    def font_style(self, value: FontStyle) -> Tailwind:
        """Utilities for controlling the style of text."""
        data = '' + value
        return data

    def font_weight(self, value: FontWeight) -> Tailwind:
        """Utilities for controlling the font weight of an element."""
        data = 'font-' + value
        return data

    def font_variant_numeric(self, value: FontVariantNumeric) -> Tailwind:
        """Utilities for controlling the variant of numbers."""
        data = '' + value
        return data

    def letter_spacing(self, value: LetterSpacing) -> Tailwind:
        """Utilities for controlling the tracking (letter spacing) of an element."""
        data = 'tracking-' + value
        return data

    def line_clamp(self, value: LineClamp) -> Tailwind:
        """Utilities for clamping text to a specific number of lines."""
        data = 'line-clamp-' + value
        return data

    def line_height(self, value: LineHeight) -> Tailwind:
        """Utilities for controlling the leading (line height) of an element."""
        data = 'leading-' + value
        return data

    def list_style_image(self, value: ListStyleImage) -> Tailwind:
        """Utilities for controlling the marker images for list items."""
        data = 'list-image' + value
        return data

    def list_style_position(self, value: ListStylePosition) -> Tailwind:
        """Utilities for controlling the position of bullets/numbers in lists."""
        data = 'list-' + value
        return data

    def list_style_type(self, value: ListStyleType) -> Tailwind:
        """Utilities for controlling the bullet/number style of a list."""
        data = 'list-' + value
        return data

    def text_align(self, value: TextAlign) -> Tailwind:
        """Utilities for controlling the alignment of text."""
        data = 'text-' + value
        return data

    def text_color(self, value: TextColor) -> Tailwind:
        """Utilities for controlling the text color of an element."""
        data = 'text-' + value
        return data

    def text_decoration(self, value: TextDecoration) -> Tailwind:
        """Utilities for controlling the decoration of text."""
        data = '' + value
        return data

    def text_decoration_color(self, value: TextDecorationColor) -> Tailwind:
        """Utilities for controlling the color of text decorations."""
        data = 'decoration-' + value
        return data

    def text_decoration_style(self, value: TextDecorationStyle) -> Tailwind:
        """Utilities for controlling the style of text decorations."""
        data = 'decoration-' + value
        return data

    def text_decoration_thickness(self, value: TextDecorationThickness) -> Tailwind:
        """Utilities for controlling the thickness of text decorations."""
        data = 'decoration-' + value
        return data

    def text_underline_offset(self, value: TextUnderlineOffset) -> Tailwind:
        """Utilities for controlling the offset of a text underline."""
        data = 'underline-offset-' + value
        return data

    def text_transform(self, value: TextTransform) -> Tailwind:
        """Utilities for controlling the transformation of text."""
        data = '' + value
        return data

    def text_overflow(self, value: TextOverflow) -> Tailwind:
        """Utilities for controlling text overflow in an element."""
        data = '' + value
        return data

    def text_indent(self, value: TextIndent) -> Tailwind:
        """Utilities for controlling the amount of empty space shown before text in a block."""
        data = 'indent-' + value
        return data

    def vertical_align(self, value: VerticalAlign) -> Tailwind:
        """Utilities for controlling the vertical alignment of an inline or table-cell box."""
        data = 'align-' + value
        return data

    def whitespace(self, value: Whitespace) -> Tailwind:
        """Utilities for controlling an element's white-space property."""
        data = 'whitespace-' + value
        return data

    def word_break(self, value: WordBreak) -> Tailwind:
        """Utilities for controlling word breaks in an element."""
        data = 'break-' + value
        return data

    def hyphens(self, value: Hyphens) -> Tailwind:
        """Utilities for controlling how words should be hyphenated."""
        data = 'hyphens-' + value
        return data

    def content(self, value: Content) -> Tailwind:
        """Utilities for controlling the content of the before and after pseudo-elements."""
        data = 'content' + value
        return data

    def background_attachment(self, value: BackgroundAttachment) -> Tailwind:
        """Utilities for controlling how a background image behaves when scrolling."""
        data = 'bg-' + value
        return data

    def background_clip(self, value: BackgroundClip) -> Tailwind:
        """Utilities for controlling the bounding box of an element's background."""
        data = 'bg-clip-' + value
        return data

    def background_color(self, value: BackgroundColor) -> Tailwind:
        """Utilities for controlling an element's background color."""
        data = 'bg-' + value
        return data

    def background_origin(self, value: BackgroundOrigin) -> Tailwind:
        """Utilities for controlling how an element's background is positioned relative to borders, padding, and content."""
        data = 'bg-origin-' + value
        return data

    def background_position(self, value: BackgroundPosition) -> Tailwind:
        """Utilities for controlling the position of an element's background image."""
        data = 'bg-' + value
        return data

    def background_repeat(self, value: BackgroundRepeat) -> Tailwind:
        """Utilities for controlling the repetition of an element's background image."""
        data = 'bg-' + value
        return data

    def background_size(self, value: BackgroundSize) -> Tailwind:
        """Utilities for controlling the background size of an element's background image."""
        data = 'bg-' + value
        return data

    def background_image(self, value: BackgroundImage) -> Tailwind:
        """Utilities for controlling an element's background image."""
        data = 'bg-' + value
        return data

    def gradient_color_stops(self, value: GradientColorStops) -> Tailwind:
        """Utilities for controlling the color stops in background gradients."""
        data = '' + value
        return data

    def border_radius(self, value: BorderRadius) -> Tailwind:
        """Utilities for controlling the border radius of an element."""
        data = 'rounded-' + value if value else 'rounded'
        return data

    def border_width(self, value: BorderWidth) -> Tailwind:
        """Utilities for controlling the width of an element's borders."""
        data = 'border-' + value if value else 'border'
        return data

    def border_color(self, value: BorderColor) -> Tailwind:
        """Utilities for controlling the color of an element's borders."""
        data = 'border-' + value
        return data

    def border_style(self, value: BorderStyle) -> Tailwind:
        """Utilities for controlling the style of an element's borders."""
        data = 'border-' + value
        return data

    def divide_width(self, value: DivideWidth) -> Tailwind:
        """Utilities for controlling the border width between elements."""
        data = 'divide-' + value
        return data

    def divide_color(self, value: DivideColor) -> Tailwind:
        """Utilities for controlling the border color between elements."""
        data = 'divide-' + value
        return data

    def divide_style(self, value: DivideStyle) -> Tailwind:
        """Utilities for controlling the border style between elements."""
        data = 'divide-' + value
        return data

    def outline_width(self, value: OutlineWidth) -> Tailwind:
        """Utilities for controlling the width of an element's outline."""
        data = 'outline-' + value
        return data

    def outline_color(self, value: OutlineColor) -> Tailwind:
        """Utilities for controlling the color of an element's outline."""
        data = 'outline-' + value
        return data

    def outline_style(self, value: OutlineStyle) -> Tailwind:
        """Utilities for controlling the style of an element's outline."""
        data = 'outline-' + value if value else 'outline'
        return data

    def outline_offset(self, value: OutlineOffset) -> Tailwind:
        """Utilities for controlling the offset of an element's outline."""
        data = 'outline-offset-' + value
        return data

    def ring_width(self, value: RingWidth) -> Tailwind:
        """Utilities for creating outline rings with box-shadows."""
        data = 'ring-' + value if value else 'ring'
        return data

    def ring_color(self, value: RingColor) -> Tailwind:
        """Utilities for setting the color of outline rings."""
        data = 'ring-' + value
        return data

    def ring_offset_width(self, value: RingOffsetWidth) -> Tailwind:
        """Utilities for simulating an offset when adding outline rings."""
        data = 'ring-offset-' + value
        return data

    def ring_offset_color(self, value: RingOffsetColor) -> Tailwind:
        """Utilities for setting the color of outline ring offsets."""
        data = 'ring-offset-' + value
        return data

    def box_shadow(self, value: BoxShadow) -> Tailwind:
        """Utilities for controlling the box shadow of an element."""
        data = 'shadow-' + value if value else 'shadow'
        return data

    def box_shadow_color(self, value: BoxShadowColor) -> Tailwind:
        """Utilities for controlling the color of a box shadow."""
        data = 'shadow-' + value
        return data

    def opacity(self, value: Opacity) -> Tailwind:
        """Utilities for controlling the opacity of an element."""
        data = 'opacity-' + value
        return data

    def mix_blend_mode(self, value: MixBlendMode) -> Tailwind:
        """Utilities for controlling how an element should blend with the background."""
        data = 'mix-blend-' + value
        return data

    def background_blend_mode(self, value: BackgroundBlendMode) -> Tailwind:
        """Utilities for controlling how an element's background image should blend with its background color."""
        data = 'bg-blend-' + value
        return data

    def blur(self, value: Blur) -> Tailwind:
        """Utilities for applying blur filters to an element."""
        data = 'blur-' + value if value else 'blur'
        return data

    def brightness(self, value: Brightness) -> Tailwind:
        """Utilities for applying brightness filters to an element."""
        data = 'brightness-' + value
        return data

    def contrast(self, value: Contrast) -> Tailwind:
        """Utilities for applying contrast filters to an element."""
        data = 'contrast-' + value
        return data

    def drop_shadow(self, value: DropShadow) -> Tailwind:
        """Utilities for applying drop-shadow filters to an element."""
        data = 'drop-shadow-' + value if value else 'drop-shadow'
        return data

    def grayscale(self, value: Grayscale) -> Tailwind:
        """Utilities for applying grayscale filters to an element."""
        data = 'grayscale-' + value if value else 'grayscale'
        return data

    def hue_rotate(self, value: HueRotate) -> Tailwind:
        """Utilities for applying hue-rotate filters to an element."""
        data = 'hue-rotate-' + value
        return data

    def invert(self, value: Invert) -> Tailwind:
        """Utilities for applying invert filters to an element."""
        data = 'invert-' + value if value else 'invert'
        return data

    def saturate(self, value: Saturate) -> Tailwind:
        """Utilities for applying saturation filters to an element."""
        data = 'saturate-' + value
        return data

    def sepia(self, value: Sepia) -> Tailwind:
        """Utilities for applying sepia filters to an element."""
        data = 'sepia-' + value if value else 'sepia'
        return data

    def backdrop_blur(self, value: BackdropBlur) -> Tailwind:
        """Utilities for applying backdrop blur filters to an element."""
        data = 'backdrop-blur-' + value if value else 'backdrop-blur'
        return data

    def backdrop_brightness(self, value: BackdropBrightness) -> Tailwind:
        """Utilities for applying backdrop brightness filters to an element."""
        data = 'backdrop-brightness-' + value
        return data

    def backdrop_contrast(self, value: BackdropContrast) -> Tailwind:
        """Utilities for applying backdrop contrast filters to an element."""
        data = 'backdrop-contrast-' + value
        return data

    def backdrop_grayscale(self, value: BackdropGrayscale) -> Tailwind:
        """Utilities for applying backdrop grayscale filters to an element."""
        data = 'backdrop-grayscale-' + value if value else 'backdrop-grayscale'
        return data

    def backdrop_hue_rotate(self, value: BackdropHueRotate) -> Tailwind:
        """Utilities for applying backdrop hue-rotate filters to an element."""
        data = 'backdrop-hue-rotate-' + value
        return data

    def backdrop_invert(self, value: BackdropInvert) -> Tailwind:
        """Utilities for applying backdrop invert filters to an element."""
        data = 'backdrop-invert-' + value if value else 'backdrop-invert'
        return data

    def backdrop_opacity(self, value: BackdropOpacity) -> Tailwind:
        """Utilities for applying backdrop opacity filters to an element."""
        data = 'backdrop-opacity-' + value
        return data

    def backdrop_saturate(self, value: BackdropSaturate) -> Tailwind:
        """Utilities for applying backdrop saturation filters to an element."""
        data = 'backdrop-saturate-' + value
        return data

    def backdrop_sepia(self, value: BackdropSepia) -> Tailwind:
        """Utilities for applying backdrop sepia filters to an element."""
        data = 'backdrop-sepia-' + value if value else 'backdrop-sepia'
        return data

    def border_collapse(self, value: BorderCollapse) -> Tailwind:
        """Utilities for controlling whether table borders should collapse or be separated."""
        data = 'border-' + value
        return data

    def border_spacing(self, value: BorderSpacing) -> Tailwind:
        """Utilities for controlling the spacing between table borders."""
        data = 'border-spacing-' + value
        return data

    def table_layout(self, value: TableLayout) -> Tailwind:
        """Utilities for controlling the table layout algorithm."""
        data = 'table-' + value
        return data

    def caption_side(self, value: CaptionSide) -> Tailwind:
        """Utilities for controlling the alignment of a caption element inside of a table."""
        data = 'caption-' + value
        return data

    def transition_property(self, value: TransitionProperty) -> Tailwind:
        """Utilities for controlling which CSS properties transition."""
        data = 'transition-' + value if value else 'transition'
        return data

    def transition_duration(self, value: TransitionDuration) -> Tailwind:
        """Utilities for controlling the duration of CSS transitions."""
        data = 'duration-' + value
        return data

    def transition_timing_function(self, value: TransitionTimingFunction) -> Tailwind:
        """Utilities for controlling the easing of CSS transitions."""
        data = 'ease-' + value
        return data

    def transition_delay(self, value: TransitionDelay) -> Tailwind:
        """Utilities for controlling the delay of CSS transitions."""
        data = 'delay-' + value
        return data

    def animation(self, value: Animation) -> Tailwind:
        """Utilities for animating elements with CSS animations."""
        data = 'animate-' + value
        return data

    def scale(self, value: Scale) -> Tailwind:
        """Utilities for scaling elements with transform."""
        data = 'scale-' + value
        return data

    def rotate(self, value: Rotate) -> Tailwind:
        """Utilities for rotating elements with transform."""
        data = 'rotate-' + value
        return data

    def translate(self, value: Translate) -> Tailwind:
        """Utilities for translating elements with transform."""
        data = 'translate-' + value
        return data

    def skew(self, value: Skew) -> Tailwind:
        """Utilities for skewing elements with transform."""
        data = 'skew-' + value
        return data

    def transform_origin(self, value: TransformOrigin) -> Tailwind:
        """Utilities for specifying the origin for an element's transformations."""
        data = 'origin-' + value
        return data

    def accent_color(self, value: AccentColor) -> Tailwind:
        """Utilities for controlling the accented color of a form control."""
        data = 'accent-' + value
        return data

    def appearance(self, value: Appearance) -> Tailwind:
        """Utilities for suppressing native form control styling."""
        data = 'appearance' + value
        return data

    def cursor(self, value: Cursor) -> Tailwind:
        """Utilities for controlling the cursor style when hovering over an element."""
        data = 'cursor-' + value
        return data

    def caret_color(self, value: CaretColor) -> Tailwind:
        """Utilities for controlling the color of the text input cursor."""
        data = 'caret-' + value
        return data

    def pointer_events(self, value: PointerEvents) -> Tailwind:
        """Utilities for controlling whether an element responds to pointer events."""
        data = 'pointer-events-' + value
        return data

    def resize(self, value: Resize) -> Tailwind:
        """Utilities for controlling how an element can be resized."""
        data = 'resize-' + value if value else 'resize'
        return data

    def scroll_behavior(self, value: ScrollBehavior) -> Tailwind:
        """Utilities for controlling the scroll behavior of an element."""
        data = 'scroll-' + value
        return data

    def scroll_margin(self, value: ScrollMargin) -> Tailwind:
        """Utilities for controlling the scroll offset around items in a snap container."""
        data = 'scroll-' + value
        return data

    def scroll_padding(self, value: ScrollPadding) -> Tailwind:
        """Utilities for controlling an element's scroll offset within a snap container."""
        data = 'scroll-' + value
        return data

    def scroll_snap_align(self, value: ScrollSnapAlign) -> Tailwind:
        """Utilities for controlling the scroll snap alignment of an element."""
        data = 'snap-' + value
        return data

    def scroll_snap_stop(self, value: ScrollSnapStop) -> Tailwind:
        """Utilities for controlling whether you can skip past possible snap positions."""
        data = 'snap-' + value
        return data

    def scroll_snap_type(self, value: ScrollSnapType) -> Tailwind:
        """Utilities for controlling how strictly snap points are enforced in a snap container."""
        data = 'snap-' + value
        return data

    def touch_action(self, value: TouchAction) -> Tailwind:
        """Utilities for controlling how an element can be scrolled and zoomed on touchscreens."""
        data = 'touch-' + value
        return data

    def user_select(self, value: UserSelect) -> Tailwind:
        """Utilities for controlling whether the user can select text in an element."""
        data = 'select-' + value
        return data

    def will_change(self, value: WillChange) -> Tailwind:
        """Utilities for optimizing upcoming animations of elements that are expected to change."""
        data = 'will-change-' + value
        return data

    def fill(self, value: Fill) -> Tailwind:
        """Utilities for styling the fill of SVG elements."""
        data = 'fill-' + value
        return data

    def stroke(self, value: Stroke) -> Tailwind:
        """Utilities for styling the stroke of SVG elements."""
        data = 'stroke-' + value
        return data

    def stroke_width(self, value: StrokeWidth) -> Tailwind:
        """Utilities for styling the stroke width of SVG elements."""
        data = 'stroke-' + value
        return data

    def screen_readers(self, value: ScreenReaders) -> Tailwind:
        """Utilities for improving accessibility with screen readers."""
        data = '' + value
        return data
