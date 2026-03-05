import io
import annotationlib
from ..serializer import Serializer, Format
from ..object import SerializableObject


# Has to be lazy due to circular imports
class SerialiableObjectSerializer(Serializer):
    def sizeof(self, format: Format) -> int | None:
        from ..serialise import sizeof

        annotations = annotationlib.get_annotations(format)
        total_size = 0
        for field_key, field_format in annotations.items():
            field_size = sizeof(field_format)
            print(field_size)
            if field_size is None:
                return None
            else:
                total_size += field_size

        return total_size

    def write(self, buf: io.Writer, format: type, value: SerializableObject):
        from ..serialise import write_serializable

        annotations = annotationlib.get_annotations(format)
        for field_key, field_format in annotations.items():
            field_value = getattr(value, field_key)
            write_serializable(buf, field_format, field_value)

    def read(self, buf: io.Reader, format: type) -> SerializableObject:
        from ..serialise import read_serializable

        annotations = annotationlib.get_annotations(format)
        attrs = {}
        for field_key, field_format in annotations.items():
            field_value = read_serializable(buf, field_format)
            attrs[field_key] = field_value

        return format(**attrs)
