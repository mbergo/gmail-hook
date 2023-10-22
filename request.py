import requests
import json

print(
    requests.post(
        "http://127.0.0.1:10000",
        json={
            "from_email": "gates@microsoft.com",
                        "content": """In the quaint town of Larkspur, nestled amidst rolling hills and serene lakes, lived Eleanor and Samuel. They had grown up together, their homes separated only by a white picket fence and a blossoming cherry tree. As children, they had shared countless adventures, from chasing fireflies on summer nights to building snowmen in winter's embrace.
            Inseparable, they were the best of friends, and as they grew older, their bond only grew stronger. But as they entered their teenage years, Eleanor began to see Samuel in a different light. She found herself drawn to his easy smile, his infectious laugh, and the way his eyes sparkled when he spoke of his dreams.
            Samuel, for his part, remained oblivious to Eleanor's growing feelings. He saw her only as his best friend, his confidante, and the one person who truly understood him.
            Despite her unrequited love, Eleanor cherished every moment spent with Samuel. She treasured the late-night conversations, the stolen glances, and the moments when their hands would brush against each other. But as much as she longed for something more, she could never bring herself to risk their friendship.
            Years passed, and Eleanor watched as Samuel dated other girls, always hoping that one day he would see her as more than just a friend. But as much as she wished for it, that day never came.
            And so, Eleanor resigned herself to a life without Samuel as anything more than a friend. She watched as he graduated from college, started his career, and eventually settled down with the love of his life. And though her heart ached with every passing year, she knew that their friendship was a treasure worth more than any romance could ever be."""
        }
    )
)# Meeting Transcription 18-10-2023
