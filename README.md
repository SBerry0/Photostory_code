Photostory converts a set of photos into a blog based on the location, context and people in the photos.

For example - in a vacation, when you take a lot of photos, this application can take those photos and convert them into a photoblog that can be shared with family.

**Milestones:**

1. Mapping a full photo library. 

2. Identifying every face in each photo and extracting them and keeping track of which image it came from. 

3.During the first version of the face recognition,  I got it to work using OpenCV. Comparing each face to get unique facial recognition to group faces for each person. 

4. Using vectorized data for the faces, I used to group people using DBSCAN. 

5. Extracting geo data from the metadata of the photograph. Then translating the coordinates into an address or an identifiable location. 

6. Grouping people and keeping track of who was with who in each photo in each place/location. This provided the context of the photo. 

7. Displaying the face and asking for user input to name each person and then using OpenAI’s GPT 4.0 API, to spin up a story/narrative of where people were and with whom and at what time, from a specified perspective.





**Example output on an album from my recent trip to Spain:**

As I wander through the vibrant streets of Cuesta de los Ciegos, Barrio de la Latina, I can't help but be captivated by the lively atmosphere. The city buzzes with energy, and amidst the crowd, I spot a man effortlessly gliding on a skateboard. A sense of familiarity washes over me, as if that man on the skateboard could possibly be me.

I continue walking and arrive at a room filled with people. Laughter and conversation fill the air, and I find myself engaged in amusing banter with those around me. The warmth of their company brings a smile to my face, and I can't deny the possibility that these people in the room could also be me.

A sudden shift in scenery catches my attention. It seems that the man on the skateboard has taken his adventurous spirit to new heights by fearlessly riding on top of a moving train. The mix of awe and excitement coursing through me brings me to wonder if, just maybe, that daring escapade could have been me.

Day 2:

The charming city of Toledo welcomes me as I stand in Glorieta de Puerta de Bisagra. Alone with my thoughts, I soak in the rich history and architectural beauty of this place. There's a certain peace in solitude, lingering as a gentle reminder that self-discovery often finds its way through moments of solitude.

Day 3:

From Toledo to Granada, I find myself standing in the elegant Hotel Anacapri. Rashi accompanies me, and together we appreciate the view that unfolds before our eyes. At a nearby table, a woman sips her orange juice, drenching the moment in a tranquil ambiance. As I observe her, a playful thought nudges at me, creating the illusory presence of which she could possibly be me.

Day 4:

In the mesmerizing Plaza de Toros de Ronda, Rashi and I embark on a journey to immerse ourselves in the vibrant spirit of Andalucía. My eyes are drawn to a man in a hat, his cell phone held in hand, capturing memories of this captivating locale. Is it solely a coincidence, or could that man Intertwine with my own path, steering it towards a connection to these vivid moments?

My gaze shifts upwards to spot a figure on a ledge, confidently steering a skateboard, radiating fearlessness. For a fleeting moment, as if peering into a mirror, I contemplate the intriguing possibility of sharing that thrilling adventure.

Day 5:

The tranquil ambiance of Calle Profesor Javier Aristu in Sevilla lulls me into profound contemplation. Alone on this spacious street, thoughts echo and intertwine. There is solace in embracing the serenity of solitude, a cherished reminder that our own company bears the capacity for self-discovery.

Day 6:

An unknown location mystifies me as Rashi and Savinay join my journey. In a spontaneous twist, we find ourselves seated at a table, savoring plates of delectable food. Looking across, I see a man and a woman sharing laughter, their joy mirroring my own. In this shared moment of warmth, a surreal thought tickles my mind. Could those content faces be mirroring my own, reminding me of the beauty found in connection and togetherness?

As my days unfold in this fascinating tapestry, one thing remains constant - the exhilarating possibilities that lie within. With open hearts and a sense of wonder, each passing day shapes a narrative rich in experiences that intertwine seamlessly with humor, warmth, and the universal embrace of family and life's adventures.
