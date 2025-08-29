book_summaries_dict = {
    "1984": """George Orwell's *1984* is a dystopian novel set in a totalitarian state where citizens are constantly surveilled by Big Brother. Individual freedom is erased, language is manipulated through Newspeak, and independent thought is punished as “thoughtcrime.” The story follows Winston Smith, who secretly rebels against the regime by seeking truth and love, only to face crushing consequences. 
Themes: freedom vs. control, truth, resistance, isolation.""",

    "The Hobbit": """J.R.R. Tolkien's *The Hobbit* follows Bilbo Baggins, a comfort-loving hobbit drawn into a dangerous quest by Gandalf the wizard and a group of dwarves. Their goal is to reclaim a stolen treasure from the dragon Smaug. Along the way, Bilbo outsmarts trolls, goblins, and giant spiders, and discovers his inner courage, even finding the One Ring. 
Themes: adventure, courage, friendship, self-discovery.""",

    "Pride and Prejudice": """Jane Austen's *Pride and Prejudice* tells the story of Elizabeth Bennet, a witty and independent young woman, as she navigates love, family expectations, and class prejudice in early 19th-century England. Her initial dislike of the wealthy Mr. Darcy slowly transforms into admiration as both characters confront their pride and misunderstandings. 
Themes: love, pride, social class, family.""",

    "To Kill a Mockingbird": """Harper Lee's *To Kill a Mockingbird* is narrated by Scout Finch, who recalls her childhood in the racially segregated American South. Her father, Atticus Finch, defends Tom Robinson, a Black man unjustly accused of raping a white woman. The trial exposes deep racial prejudice, teaching Scout and her brother Jem about justice, morality, and empathy. 
Themes: justice, racism, morality, empathy.""",

    "The Great Gatsby": """F. Scott Fitzgerald's *The Great Gatsby* is set in the roaring 1920s and follows narrator Nick Carraway's encounters with his wealthy neighbor, Jay Gatsby. Obsessed with rekindling a past romance with Daisy Buchanan, Gatsby throws lavish parties in pursuit of a dream that ultimately collapses. The novel critiques the emptiness behind wealth and glamour. 
Themes: wealth, love, illusion, the American Dream.""",

    "Brave New World": """Aldous Huxley's *Brave New World* imagines a futuristic society where people are genetically engineered, socially conditioned, and kept content through pleasure and consumerism. Stability and conformity replace individuality, with dissenters silenced or exiled. The novel questions the price of comfort when it comes at the cost of freedom and humanity. 
Themes: technology, control, happiness, individuality.""",

    "Crime and Punishment": """Fyodor Dostoevsky's *Crime and Punishment* follows Raskolnikov, a destitute student in St. Petersburg, who convinces himself that murdering a corrupt pawnbroker is morally justified. After committing the crime, his conscience torments him, leading to paranoia, inner conflict, and eventual confession. The novel explores redemption through suffering. 
Themes: morality, guilt, punishment, redemption.""",

    "Moby-Dick": """Herman Melville's *Moby-Dick* tells of Captain Ahab's obsessive quest to hunt the great white whale, Moby Dick. Narrated by Ishmael, the novel explores the destructive power of obsession as Ahab sacrifices his crew and ship to avenge his past injury. Rich with symbolism, it reflects humanity's struggle against nature and fate. 
Themes: obsession, revenge, nature, fate.""",

    "The Catcher in the Rye": """J.D. Salinger's *The Catcher in the Rye* follows Holden Caulfield, a disillusioned teenager recently expelled from prep school. As he wanders New York City, he struggles with alienation, identity, and his longing to protect innocence from the corruption of adulthood. The novel captures adolescent confusion and rebellion. 
Themes: adolescence, alienation, identity, innocence.""",

    "Lord of the Flies": """William Golding's *Lord of the Flies* depicts a group of boys stranded on a deserted island who attempt to govern themselves. Their fragile order collapses into violence and savagery, revealing humanity's darker instincts. The novel serves as an allegory for civilization's thin veneer and the struggle between order and chaos. 
Themes: civilization vs. savagery, power, fear, human nature.""",

    "The Alchemist": """Paulo Coelho's *The Alchemist* follows Santiago, a young shepherd, who dreams of finding treasure near the Egyptian pyramids. On his journey, he meets guides and faces obstacles that teach him about listening to his heart, embracing destiny, and finding spiritual fulfillment. Ultimately, he discovers that true treasure lies within. 
Themes: destiny, dreams, self-discovery, spirituality.""",

    "Fahrenheit 451": """Ray Bradbury's *Fahrenheit 451* is set in a dystopian society where books are outlawed and firemen burn them to suppress knowledge. Guy Montag, a fireman, begins questioning his role and society's blind obedience, eventually joining rebels who preserve literature. The novel warns against censorship and conformity. 
Themes: censorship, freedom, knowledge, rebellion."""
}


async def get_summary_by_title(title: str) -> str:
    if not title:
       return "Summary not found."
     
    title = title.strip().lower()

    for t in book_summaries_dict.keys():
        if t.lower() == title:
            return book_summaries_dict[t]

    return "Summary not found."

