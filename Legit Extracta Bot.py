import streamlit as st
import os
from PyPDF2 import PdfReader
import docx
from dotenv import load_dotenv
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings.huggingface import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from langchain import HuggingFaceHub
from streamlit_chat import message
from langchain.callbacks import get_openai_callback

page_bg_img = '''
<style>

[data-testid="stSidebarContent"]{
    background: linear-gradient(0deg, #588EAD 0%, #151414 100%);   
    }
</style>
'''
st.markdown(page_bg_img, unsafe_allow_html=True)

# Define user_template as a string template
# user_template = "<div style='background-color: #3ccccf; padding: 10px; border-radius: 5px; margin: 5px 0;'>User: {{MSG}}</div>"

# user_template = "<div style='display: flex; align-items: flex-end;'><img src='data:image/png;base64,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' style='width: 30px; height: 30px; border-radius: 50%; margin-right: 10px;' alt='User Avatar'><div style='background-color: #3ccccf; padding: 10px; border-radius: 5px;'>User: {{MSG}}</div></div>"
user_template = "<div style='display: flex; align-items: center;'><img src='data:image/jpeg;base64,/9j/4AAQSkZJRgABAQAAAQABAAD/2wCEAAoHCBYWFRgWFhYYGBgaGhgcGhoaGhwcGhocGBwaGhocHBocIS4lHB4rIRgaJjgmKy8xNTU1GiQ7QDs0Py40NTEBDAwMDw8PEA8PHjEdGB0/NDE/MTExMTE/MTExMTExMTExMTExMTE0MTExMTExMTExMTExMTExMTExMTExMTExMf/AABEIALwBDAMBIgACEQEDEQH/xAAcAAADAAMBAQEAAAAAAAAAAAAAAQIDBgcFBAj/xABEEAABAgQDBAgEBAUCBQQDAAABAhEAAyExBBJBBSJRYQYHE3GBocHwMpGx8RRCYuEjUoKS0XKiM4OywtJUo9PiQ0RT/8QAFQEBAQAAAAAAAAAAAAAAAAAAAAH/xAAVEQEBAAAAAAAAAAAAAAAAAAAAAf/aAAwDAQACEQMRAD8A7AtQIIBrEShlvSAS8teEMqzUFIBTA5cVi0KAABNYkHLQ11hGXmrxgJQkggkUi5u9asHaPTjCAy1NYCpRyhjSIUkkuBSGU5qimkUJgFOEA1qBDCpiJQy3pAJeWvCGTmtRoCZgcuKxkSsAMTWJSrLQ98BlvXxgJQgguaCKm71qwGYFUGsJIy3q8BUs5QxpEKSSXajw1JzVHdD7QDd4UgKWoEMKmIlbt6QBGWp0+0BOa1GgFMTmLisZAoMz1ZokLy0MIy33n5wCloILmgipu9asBXmoPesIbt6vAVLUwY0iCku7Ud4opzVEHaAbvh6QFTFAhhUxErdd6QBOWp0gJzWo0ATEklxURYUGZ6s3jEpXloYXZ/m8fWAJaSC5oIc3eZqtAV5qCBO7er8OUA5agAxoYjKXdqO/hDKc1RD7T8vh6QDmKBDCpjF2auEWE5amK7ccDAQJhNDrFKTlqPOKWkAEi8RKLmte+AaU5qnupCMwig0gmljSndFoSCASKwCMsJqNIkHNQ+UJCiSAbRU0NandAJSstB31gyC5evv5Q5YcVr3xiUsgnhp/iAYmE0NjdtO6GoZd4a6H3eKWkJD/AC5REqp3qjgdOcBSU5t4/L/MSZhsLCn3gmuDu24DXnFhIUH5V5wCKAKh6faElWeho3CJQoqIHvui5tAMtDy0gEpeXdHfWGEC+pr94JYBFQ55/WIUogkc/nANMwmhsfnSvyhq3K3e/wC0NaQkE66H0iZP6qjR9ICgjNvH5Dh/mJ7Q6M1vvzgmODSgu3rFhIIdtH7+cAihhmGnH1hJOeho3CJQoqPLXnFztMtOLfSASl5d0e+6GEfO/LjDlgEVFfpGIqL5efswFpmE7p191gVuWq/HlDWAkGlfrCk65q8H+kBSUZqnyhdobaW9ISnBpQcOEZQkM+recBJTlqPOEnevpw5wS1EljUQ5tGandAJS8tB5xXZj4tb+sEtIIc1MRmLto/lANK81D5RXYDnBMSAHFDGLOriYCkoILkUiphzBhWDtHpxhBOWt9IByzlDGkSpBJcCkMpzVtpD7RqNaApSwQwvESxlvSAS8tXtDJzUs0BMwOXFYYWAGVdvfjDfLS+vv5RHZ5qktq3rATLQQQVCnu8VMOa1R78oO0zbvHzgAy3qDT9oAQrLQ0D+2aJWgkukU925xRTmtQW7vbxrnSPp1g8E6FzM8wU7OWylg8w7Jv+YiA2VawQyb+7xCCEglW7zPm8cM2r1sYuacmFlpkuWBbtZpJoGcZQTwCT3x8KeiW2MeQqcJjGoViVlIB5IO8nWyWgOx7T6YYCWTnxclxcJWFqBGmVDnyjyl9a2zAP8AirUW/LKX5ZgI0/A9S6mBnYtI4ploKq8lKI/6Y9zDdT2BT8c3EKOozoSPJD+cBaOt3AAuUYg90tH/AMkZx1t7PUwJnpb+aWD88qjFy+qnZ2qJvjMV6RimdUuz1W7dHApmD/uSYD1Nn9Y+zF7v4oJ5LQtP+5SWbxj3sFtGTPJMibLmJeuRaV+SS4jnOK6mMOf+HiZqOBWhKw/9OWNZ2p1TY6Uc0lUucBUZFFC3H6VUfuVAd7mLBBCffdzhS93l71j874XpVtbZ6sq1TGSWyT0laDyCzUf0qEbxsHrgkTGTipZkK1Wh1yyeJHxo8M3fAdPmJzF0191eKCwzPvW5v/iPmwWOlzEBcpaZiFWWhQUk8nFiPKPo7N95639WgJQnKXVT3RoqZvc29/OArzUsfpAnd+L/ABbWAqSrKGVT3rCKC7tR38IAkqrb1iu0/K3L0gGtQUGFTEyt13o8MIy1vAd7k3r9oCZiSouKiMmcM2rN4xIXlpeDs/zPz9YCUJKS5oIzdqOMYyvNS0H4fnAMywKjSJSc1D5QkEvV25xU0MN3ygEpWWg76xQlg1OsKUHG95xKyXo7coATMJodYpYy1HnFLAYsz8oiVX4vOAaU5qnujGpZdtB84qbQ7vlDSkKGj+cAlIHy8+6Pg2ttiTIlqmYhaUIT+Y6n+VIupXIR8PSfpLKwUkzZxOoSgHeWpqJS/mbAfKOJJRjdu4t6BKe8SpCCbDiot/qURwFA9TpJ1k4rFq/D4JK5UtRZISHxEx9HS+XuTWlzH2dGuqNammY5ZQDXskEFf9S6hPcHPMR0for0Sw+ARllJzTFDfmrAzr4j9Cf0jzNY2C3OA8zY3R/DYNLYeShFGKgHWrvUXUfEx6dq+/CC1/ty7oGavsQBzgZ68PdYG18vXvgZ6+z3wBf37pA709nugv78oL0s3l3QA+nv7wO1PfjBy998HL2e+A+bG4KWtOVaAoEa3HjwjnPSjqukqBXJBQf0C3eixH+lo6fbm8FvduXdAfm9MvHbLmdpLUUpJG+nelLGgWk0+YfgY6r0J6ypWMKZU0Jk4hgAD8EzTcUS4V+k1rQmsbHtjYiVhSkpS5BzIIGVQN6Gj/WONdK+g5TmmYZJo5VK1DXya/0/LhAd/VLA3hcWf1hJ370bhz9I5F1b9Y5Kk4XHLeyZc1Rufypmk35KPjxjr02vw04t9KQDKymgi+zDPrf1hSWIrfnEkl9WfwaAaVFVDDVu2148ocwACl+UTKq+bzgGlGapie0L5dLekOYSDS3KLYNo7eLwElATURPbnlDlkk1tzjLlTwEBKlghhcxEsZamkHZ5avaGTmpbWAUwZqisWlYAY3ESDlpfWF2ear3gElBBc2EVMOagrB2j0ZnhAZa3eAaDlDGPO2zj5eHlLxExWWXLGZSuOgSBqokgAcSI9ApzVtp7+ccR65OkSps9GBlElEsgrArnmqAypYXyg6aqPAQHhn8Vt3H/AMqdNUyJIP8AuUf9yjoLd22HseThZKZEhGVKf7lK1Uo6k/tQBo8roJ0ZTgMMlDAzlsucripvhf8AlTYc3OpjZfrAHI3+sFr/AH5R8m09pSsPLVNnrShCbqUfkEi6idAKmOZbX65EAkYfDlYqM8xWUU1CEuW1ckHlAdYFL/aAc7fSOHSeuXF5t+Rh1p4JC0n5lZ+kbn0Z608LiFCXOBwyywGchUtR4dpRv6gBzgN+b5cPWA1tb6wvp78oZ5W1/aADW3vlB3X+kB5e/wB4O6/u8ActfdYORv8AWD6x5m3dvSMHL7TETAgWSLrUeCEiqr93FoD0xz+/KAUv9uUce2n10FyJGGDaKmqL/wBibf3GPiwnXNiQf4uGkLHBBWg/NSlfSA7cPL6R5O2tm5wVoG8Lj+YD1jxeinWFhMaoS3MqabS1tvnglYoruoS1o3D6e/KA4T046LBYViJCd4VmIH5xqtI/mGo1ve+0dUfTUzU/g8Qv+KhP8JRNVoSKpPFSRUHVI5F9n2/gsi86RurvyVqB33+ccY6W7NVgsSjESCUpUrOgp/8AxrSXKeDagcCRpBX6RKcxdNoyBYZtWbxjxOim3kYrCyp6BVad9IPwrFFp8FAsdQQdY9ns/wAz8/WCJQgpLm0VM3rVaDPmpaENzm/p94CkKCQxvEZC76O/hFZM1bQdp+VuXpANagoMLxj7I8IvJlreD8RygElZJY2MNYy1EUtmLM/K8RLvvef7wDQnNUwlTCCwsIJl93y/aLQzB2fneASkBIcXESg5qGEh3q7c7RU39Pl+0B8O3NojDSJs4/DLlqW3EpBYeJAHjHDuqnZqsXtBeJmjP2RM5RP5pq1HKSO/MrvQI6B1y44y9mlFXmzUI55Q8w+G4B4x83UrguzwKppAedNWeeVACAD/AFBfzgOh2qKv5xixOIRLQuYtQSlCVKUo2CUgk/IAxltX34RovXDjjL2coJLGdMRLp/LVZ+YQx74DlPSbb8/auKo6ZYcS0E7stOqlN+Y0c8WHCPU2f0fkywHQFq1UoPXkk0EfJ0NwoTKUvVaiH/Smn1fyjYYDBNwUtQyqQgj/AEj/ABGrbY6PhLqlhiK5dCOXA8o3CPmxqaA8D9YI9Lqf6YqURgJ6yaHsFKNQEhzKfgwJS9mI/lA67agt9I/LuMmnDYtE5FClaJqRzCnI7iUn5x3MdZmy9MT/AO1P89yCtvNLe+cFqir+cagnrL2WLYp/+VP/APCAdZeyx/8AtPx/gz/LcgPf29tZGFkTMRMO6hLtqomiUDmVEDlH51nzsRtPErmzVXufyy0OcqEDQCrDvJq5jbetfplh8XKkycLN7ROdS5m4tLFKQlA30h/iXbgI+Lo3hRLw6GusZieOa3kwgMmC2LIlgZUAn+ZQCld7m3g0Z8Ts+WsMpCDwOUUj6YII0bbGxezdct2TUjVP6geEde6qumSsXLOHnqefKSCFm8yW7AnipJYE6uk3eNOxyKg8QQffjHhdC8QcLtWTlJymaJRHFM3cD8WzA94gr9CbUw+eWpA4OORFR87eMc36UbMGIwy0AOps6OIWmobvqn+qOpu1PfjGlY6XkmLTwUW7nceTQWNQ6itr/wAWdhFGi09qjkpLJWO8gpP9Bjs/aF20t6R+c9hTPwm2pYFB+IyUpuT90fITB8o/SAZtHbxeCEpISHF4SN6+nrClu9XbnbzhzdMvl+0AlKKSwtFZAz639YJbNVn5384ir6s/g3+IBpUVFjaL7EQpjNRn5X8oxOr9XnAWlBBc2ENZzUELtM1GZ4eXLW+nCAEHLQwlIJLixh5c1bacYO0ajO0A1LBDC5iUDLUw+zaru0D5qWbxgOV9fS3w+Gaxmr+YT/8AYxsvVegI2XheaVnxVMmFvOPA69cMfwkhV8s9ieAWhV/7RHq9UmJC9mSQ7lCpqDy31LA/tWmA3QUqftHP+urBqXs8LFpc5C1DkoLR9VpjoA5205d8fHtXZycRJmSZgOSYhSTxDiih3FiOYEBwjofOCsPl1QpQI/1bwPmflHuxpc2RO2bilypqTQsdBMQ+6tB1BuPEHVtswWNRNTmQoKGo1HIi4MEfRHz41W63OPoJaNc23ttKXCSFKsBw5q/xAeJtpBm4lKEB1HIgDipRoPmoCOrHqZwwocRPfRgj/wAY1vqk6LqxE8YyaD2cpRVLf883Qh9EneJ4hPOO5d9/doK5iepnCi+In/JF/wC2A9TOG1xE/wCSP/GOnDn7/eAc7acu+A/P3WN0FRs9Mlcpa5iJilpUV5d1QCSkboFxn/tj69gTgrDyyNEhJ707p+kdZ6ZbAGNwi5BYKoqWo/kWl8pPAFyk8lGPz/svHLwc1cmehSQFMtJG8hQo/Md1wxHMN3giMPPQtOZKgpJ1Bf2YpawkOYI+bHKsO+Na6NSDiNqyAn/1CFf0yiFqP9qDFbc22N5KC6jQkWSOR1Mb51NdF1ICsdNSQVpyyEmhyn4pnIFmB4ZtCIK6vahq/nGo7bDT1/0/9KY27vv7tGn7XW85ZPFv7QB6QWOQ9JdzaqVChz4dXiAj/EfpIyy76O8fm7Hp7bbKECr4iQji2UoSr5EGP0kZv5W5ekENSgoMLwkbt9YMmWt4Pi5N43+0AlJKi4tFdoGbW3jaFny0vB2f5n5t5wCSkpLm0ZO2ERnzUtB2HPygGpAAcXESg5qGEgF6u3O0VNtu+X7QCWctBFJQCHNzBKtvX5/vEKBejtytANKySxsYaxlqIpZDUZ+V4iV+rz/eA13p7sk4vZ+IlgOsJzoAuVSyFhI5lin+qOc9R22UpXOwiz8f8WX/AKkjLMHeUhJ7kGOzzXfd8v2j8+9PtizNmY5OIkOlC19pKULJUC6pZHB9DdJbQwHfxW/hz74PpHg9D+k0vHyBMQyVhhNlvvIX/wCJuDr3giPefTz9IDw+lHRfD49AROSXS+SYmi0E3ynVPFJcfIEcj2t1T46Soqw6kT0ixSoS1+KVED5KMd4dqexBag+0B+dU9Btrr3TJmkH+aajL5raNr6OdUBzBeNmJI/8A4yia2oqYWyi7hI8RHX7c39vBavHz7oDFhsMiWhKEJCEoASlKQwSBZIA0jL33+ndBz190gvWzeXfAA5++cA5+HPvgvf3zgvQ/eAPpGq9Meg+Hx4zKeXNSGTNSATySpP50jwI0IrG1Pp5+nfA7U9iA4DtDqw2lIUTJCZo/mlTAlTaOlRSX5B4+WX0B2tNISuUtjrMmpyjnVZPyBj9EWoPtBbn7vAcv6K9U0uURMxi0zlBimUl+zBH8xLFY5MBxe0dPAAHBqd3IDhDtXj5wc9fdIDHPmhCVLV+UE/bvjQNp48S0LnLskKWeZ4DmSW8Y2LpBj8x7NJoDvd40/wA/tHF+nPSH8QsYeS6kJUHKa512CUtdIfxPcIK+3qmwCsRtL8QqolBc1R0zrdKR81FX9EfoIIDPqz+N41Lq16NDA4QJWAJ0whc12cFt1L8EineVcY2ogvqz+Df4ghpUVFjaGvdtrDmENRn5X8omVrm8H/eApKQoObxOcu2jt4WgmO9Hblbyi3DaO3i8AlJCQ4vGPtjFS3ertzt5xldPLygIUsEMLmEkZamDs8tXtCCs1LawDWnNUd0NMwAMbiJKstL6w+zer3gJSgpLmwilnNQQhMzUZnhkZa3eAEHKGPfHl7e2JLxspUqal0KsfzJVopJ0I90j02zVtp7+cSqY1BpR+PKA/Oe09mY3YuJExCjldkTAP4cxNyhadCwqk1o4NAY6r0R6xsNjAlCyJE80yKLIUafAs0JOiSx72eNwxmAlzEKQtCVoIZSVJBSRwIPvWOT9JeqLMVLwK21MiYT/ALZh8gr+6A67anvxgt7+sfnvDdJNq7LV2UwLCRQS56SqWWb4Fu7D9Cmjc9j9ckhQbEYdaDqqWQtPeUnKUjkM0B1G3v3SBmr78I1vZ3TrZ834cVLB4TCZZHLfAfwjYMPPQsZkLStOmVQUB8jAZG19/eBnr78YG1anD1gNai31gC/v3SC9PfhAa298oL2p6QBygdqe/GDlr7rAaX+/OALe/rBb37pHnY3b2Gk/8bEyUH9UxAJ5ZXeNT2r1rYCU4lqXiFWGRJCR/UtnHMPAb6aVPjyjWekXSeXJQVZ0oTqsnyQLqV3eHGOUbd60cTPdMpKZSTYfEeTCz94MYdk9Bdo49YXOCpaTeZPcFnrlR8R5UA5wGDpJ0wXiT2GHCkoUcrgfxJj0CQBYEmwqfKN96tOrv8OU4rFp/i3ly79mf5lfrrQad9tn6KdBMNgAFoBmTWYzFgZi9DlFkCulTqTG0fHaje2gGRmLiLzhm1t6RIXl3QIfZ/mfn6wCSkpLm0Ne9bT1gC81LQHd5v6feAEqCQxvCyF30v6wwjNW0Haflbl6QApQUGF4nsDyismWt4PxHKAlKySxsYqYMtRSKWQQWZ+URLoa+cA5YzBzWJUsgsLCHMqaeUWhQYOzwApAAcXERLOa9YSAQQ7tziptfh8oBTFZaCkAQCHF9ffGHLLDep3xiWC+67e6wAlZJA9+MVMASBlofOKWQ27UnziJVKm/PXlASuQiakpmISsGhSoAg+BoRGnbW6ttnzSf4Rkq4yVFI8El0/7Y3OaHqPLTlFpIbeYEC3DnAch2j1JgOZOLIGiZkt/mtKh/0xr6+qXaCDmQqSsixRMUk/7kpb5x3qWC4zO3P6xcwuwFRy1gPz8rovt6UGH4kD9GJBDdyZkWEdIUf+uPipY9Y79LUwY0rr9P3jGsF6O3kIDgiMf0hsBjfCUT/wBsH4npCdMaP+WU/wDaI7/MIZk1PAfWFLpU68dYDgA2V0hmG+M8ZxR9ViJPV/tecWmgjT+LiEq8gpRj9ATA9U17vpFpIapGZvEHhAcOwvUvibzcRJQP0Baz5hI842XY/U9hEF582bNI0DS0nvAdQ/ujpEsF3U4bjpzipm8zeX1gPH2Z0bwuEI/D4eWilFZcy/FanV5x7QQCH0v4/wCIUo0ZXnrGMgvrle/p+8A0LKi2mv7RUzdbLR7+zrFTFBmT5aRMvdf1+sBUpIUHNTCKy7aO3hCUly6ajlGUEM1HbxeAS0hIcUMTL3nere9IJYINbc4c2rZfKAlaiksKCMmQM+rP4wpZAFb84jKXerP4NACFFRY1EZexTw+sTMIIpflGLKrgYCkyyKnSKWc1B5whMzUa8Mpy1FdIASctD30hGWTUawwnNU00hGZlo1oCjMCqDWJSMtT5Q+zy14Qgc1LNACk5qjurB2gTT39oCrLS+sCZT14wEJllO8a8W9IajmqL+7Q0renHy1gy5a3eAEnLe9/vEmWVb1tRx8YrJmrbSBS2pwp3wApYVu+/tCRu0PlyilSmrw+0A3qWbhAQpOa1rV93ihMCd3w7u+B8tL6wxKcPxrAQlBTW48+Hyhrrbx/aGleanH0rBly1FX8oBBWW9+Vm/wAwjLJ3qcfvFBGbety9YCtizcoBKWFUFDo/zrAil/L3aGqU1eENs3JvWAhQKjS31bhFCYBu+D6Q1Ky7og7Gj+PrAQlJSeX0fjDXW3n7tDC81OMPLktV/SAEHLQ35QuzL5tL+sNKM1bQ+0/K3L0gArCqCBO7fXhygKMtbwDevRvX7QApOaoh9oGy629IRXlpeDs/zePrACU5amK7cc4kLzUtD7AcYBqQAHArESzmoaxEr4hGXEWHfATMLFhSLSgEORWFIt4xim/EYCkKJLE0ipgy2pGSbYxiw1zAOWMwc1iVLILA0hz7+EZZfwjugJWkAOLxEo5r1iJPxCMuIsICJispYUjIlAIcisKRbxjEv4j3wFIWSWNRFTd21Iud8J96xGG1gHLDhzWIUsgs9LQ59/CMqPhHdAStIAcUMRKOa9YmV8Q96ReIsICZispYUEZAgM7VZ4JFvGMKvi8YCkLJLGoipu7akXO+E+9YjDawDlpCg5qYgrLs9HbwgxF/CMw+Hw9ICFpCQ4oYmVvO9WiZHxReI08YCZiiksKCMgQGdqs/jBItGE/F4+sBSFFRY1EVN3Wajxc/4YjDa+HrAOWkKDmpiM5dno7eEE+8Zvy+HpAQtISHFDGLtVcfpFSLx9MB/9k=' style='width: 30px; height: 30px; border-radius: 50%; margin-right: 10px;' alt='User Avatar'><div style='background-color: #588EAD; padding: 10px; border-radius: 5px;'>User: {{MSG}}</div></div>"

# Define bot_template as a string template
bot_template = "<div style='background-color: #028d99; padding: 10px; border-radius: 5px; margin: 5px 0;'>Bot: {{MSG}}</div>"



# "with" notation
def main():
    load_dotenv()
    st.header("💬 LEGIT EXTRACTA BOT")

    if "conversation" not in st.session_state:
        st.session_state.conversation = None
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = None
    if "processComplete" not in st.session_state:
        st.session_state.processComplete = None

    with st.sidebar:
        uploaded_files =  st.file_uploader("Upload your file",type=['pdf','docx'],accept_multiple_files=True)
        # openai_api_key = st.text_input("OpenAI API Key", key="chatbot_api_key", type="password")
        process = st.button("Process")
    if process:
        # if not openai_api_key:
        #     st.info("Please add your OpenAI API key to continue.")
        #     st.stop()
        files_text = get_files_text(uploaded_files)
        # get text chunks
        text_chunks = get_text_chunks(files_text)
        # create vetore stores
        vetorestore = get_vectorstore(text_chunks)
         # create conversation chain
        st.session_state.conversation = get_conversation_chain(vetorestore) #for huggingface

        st.session_state.processComplete = True

    if  st.session_state.processComplete == True:
        user_question = st.chat_input("Ask Question about your files.")
        if user_question:
            handel_userinput(user_question)






def get_files_text(uploaded_files):
    text = ""
    for uploaded_file in uploaded_files:
        split_tup = os.path.splitext(uploaded_file.name)
        file_extension = split_tup[1]
        if file_extension == ".pdf":
            text += get_pdf_text(uploaded_file)
        elif file_extension == ".docx":
            text += get_docx_text(uploaded_file)
        else:
            text += get_csv_text(uploaded_file)
    return text


def get_pdf_text(pdf):
    pdf_reader = PdfReader(pdf)
    text = ""
    for page in pdf_reader.pages:
        text += page.extract_text()
    return text

def get_docx_text(file):
    doc = docx.Document(file)
    allText = []
    for docpara in doc.paragraphs:
        allText.append(docpara.text)
    text = ' '.join(allText)
    return text

def get_csv_text(file):
    return "a"

def get_text_chunks(text):
    # spilit ito chuncks
    text_splitter = CharacterTextSplitter(
        separator="\n",
        chunk_size=900,
        chunk_overlap=100,
        length_function=len
    )
    chunks = text_splitter.split_text(text)
    return chunks


def get_vectorstore(text_chunks):
    embeddings = HuggingFaceEmbeddings()
    knowledge_base = FAISS.from_texts(text_chunks,embeddings)
    return knowledge_base



def get_conversation_chain(vetorestore):
    llm = HuggingFaceHub(repo_id="vennify/t5-base-grammar-correction",  huggingfacehub_api_token="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", model_kwargs={"temperature":5,
                                                      "max_length":100})
    memory = ConversationBufferMemory(memory_key='chat_history', return_messages=True)
    conversation_chain = ConversationalRetrievalChain.from_llm(
        llm=llm,
        retriever=vetorestore.as_retriever(),
        memory=memory
    )
    return conversation_chain

def handel_userinput(user_question):
    with get_openai_callback() as cb:
        response = st.session_state.conversation({'question':user_question})
    st.session_state.chat_history = response['chat_history']

    # Layout of input/response containers
    response_container = st.container()

    with response_container:
        
        for i, message in enumerate(st.session_state.chat_history):
            if i % 2 == 0:
                st.write(user_template.replace("{{MSG}}",message.content),unsafe_allow_html=True)
            else:
                st.write(bot_template.replace("{{MSG}}",message.content),unsafe_allow_html=True)




if __name__ == '__main__':
    main()






