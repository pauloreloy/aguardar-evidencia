
class Utils:


    @staticmethod
    def _convert_to_dict(payload, ctx):
        if payload is None:
            return {}
        if isinstance(payload, dict):
            return payload
        try:
            return dict(payload)
        except Exception:
            raise ValueError("Payload invalido")
    