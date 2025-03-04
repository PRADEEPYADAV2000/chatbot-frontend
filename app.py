from flask import Flask, request, jsonify
from flask_cors import CORS
import difflib  # For fuzzy matching

app = Flask(__name__)
CORS(app)  # Enable CORS

# Sample dataset
dataset = [
      {"question": "What is Artificial Intelligence?", "answer": "Artificial Intelligence (AI) is the simulation of human intelligence in machines."},
        {"question": "Who is the Prime Minister of India?", "answer": "The Prime Minister of India is Narendra Modi (as of 2024)."},
        {"question": "What is Python?", "answer": "Python is a high-level programming language used for various applications."},
        {"question": "What is the capital of France?", "answer": "The capital of France is Paris."},
        {"question": "Who discovered gravity?", "answer": "Gravity was discovered by Sir Isaac Newton."},
        {"question": "What is the speed of light?", "answer": "The speed of light is approximately 299,792,458 meters per second."},
        {"question": "What is blockchain?", "answer": "Blockchain is a decentralized digital ledger that records transactions securely."},
        {"question": "What is IoT?", "answer": "IoT (Internet of Things) refers to interconnected devices communicating over the internet."},
        {"question": "Who invented the telephone?", "answer": "The telephone was invented by Alexander Graham Bell."},
        {"question": "What is quantum computing?", "answer": "Quantum computing uses quantum mechanics principles to perform calculations."},
        {"question": "What is machine learning?", "answer": "Machine learning is a subset of AI that enables systems to learn from data."},
        {"question": "What is deep learning?", "answer": "Deep learning is a subset of ML using neural networks to model complex patterns."},
        {"question": "What is the largest planet in our solar system?", "answer": "Jupiter is the largest planet in our solar system."},
        {"question": "What is photosynthesis?", "answer": "Photosynthesis is the process by which plants convert sunlight into energy."},
        {"question": "Who wrote Hamlet?", "answer": "Hamlet was written by William Shakespeare."},
        {"question": "What is the boiling point of water?", "answer": "Water boils at 100°C (212°F) at sea level."},
        {"question": "What is the chemical formula for water?", "answer": "The chemical formula for water is H2O."},
        {"question": "What is the human body's largest organ?", "answer": "The skin is the largest organ of the human body."},
        {"question": "What is the powerhouse of the cell?", "answer": "The mitochondrion is known as the powerhouse of the cell."},
        {"question": "Who painted the Mona Lisa?", "answer": "The Mona Lisa was painted by Leonardo da Vinci."},


        
    {
        "question": "What is the Indian Penal Code (IPC)?",
        "answer": "The Indian Penal Code (IPC), enacted in 1860, is the primary criminal code of India. It defines various crimes, including murder (Section 302), theft (Section 378), and defamation (Section 499), along with corresponding punishments. It applies across India, except for Jammu and Kashmir, which follows the Ranbir Penal Code."
    },
    {
        "question": "What is the Code of Criminal Procedure (CrPC)?",
        "answer": "The Code of Criminal Procedure (CrPC), 1973, lays down the procedures for criminal trials in India. It classifies offenses as cognizable and non-cognizable, outlines the powers of police and magistrates, and details the process for arrest, investigation, bail (Section 437), and trials."
    },
    {
        "question": "What is the Code of Civil Procedure (CPC)?",
        "answer": "The Code of Civil Procedure (CPC), 1908, regulates the process of civil litigation in India. It defines procedures for filing civil suits, jurisdiction (Section 20), appeals, and execution of decrees, ensuring fair trial and justice in non-criminal disputes."
    },
    {
        "question": "What is the Indian Contract Act, 1872?",
        "answer": "The Indian Contract Act, 1872, governs contractual relationships in India. It defines essential elements of a valid contract (offer, acceptance, consideration), types of contracts (valid, void, voidable), and remedies for breach of contract (Section 73)."
    },
    {
        "question": "What is the Information Technology (IT) Act, 2000?",
        "answer": "The IT Act, 2000, regulates cyber laws in India. It covers electronic contracts, digital signatures, hacking (Section 66), identity theft (Section 66C), cyber terrorism (Section 66F), and data protection. It also provides legal recognition to electronic records and transactions."
    },
    {
        "question": "What is the Right to Information (RTI) Act, 2005?",
        "answer": "The RTI Act, 2005, empowers Indian citizens to seek information from government bodies to ensure transparency and accountability. It mandates public authorities to provide information within 30 days, with some exceptions related to national security and privacy (Section 8)."
    },
    {
        "question": "What is the Goods and Services Tax (GST) Act, 2017?",
        "answer": "The GST Act, 2017, replaced multiple indirect taxes with a single tax structure. It classifies goods and services into different tax slabs (0%, 5%, 12%, 18%, and 28%), introduces Input Tax Credit (ITC), and mandates GST registration for businesses with an annual turnover above ₹40 lakh (₹20 lakh for services)."
    },
    {
        "question": "What is the Consumer Protection Act, 2019?",
        "answer": "The Consumer Protection Act, 2019, safeguards consumer rights against unfair trade practices. It establishes Consumer Disputes Redressal Commissions at district, state, and national levels and covers e-commerce transactions. It also introduces provisions for misleading advertisements and product liability."
    },
    {
        "question": "What is the Companies Act, 2013?",
        "answer": "The Companies Act, 2013, regulates corporate governance and company registration in India. It defines company types (private, public, OPC), compliance requirements, director responsibilities, and corporate social responsibility (CSR) provisions (Section 135)."
    },
    {
        "question": "What is the Prevention of Corruption Act, 1988?",
        "answer": "The Prevention of Corruption Act, 1988, criminalizes bribery and corruption by public officials. It includes offenses such as accepting bribes (Section 7), misusing office for personal gain, and disproportionate assets. The 2018 amendment expands the scope to private entities."
    },
    {
        "question": "What is the Protection of Children from Sexual Offences (POCSO) Act, 2012?",
        "answer": "The POCSO Act, 2012, protects children from sexual abuse and exploitation. It defines offenses like sexual assault (Section 7), aggravated assault (Section 9), and child pornography (Section 14), with strict punishments, including life imprisonment in severe cases."
    },
    {
        "question": "What is the Dowry Prohibition Act, 1961?",
        "answer": "The Dowry Prohibition Act, 1961, criminalizes the giving and receiving of dowry in India. Section 3 prescribes imprisonment of up to five years and a fine for violating this law. The act is aimed at preventing dowry-related harassment and deaths."
    },
    {
        "question": "What is the Domestic Violence Act, 2005?",
        "answer": "The Protection of Women from Domestic Violence Act, 2005, provides legal protection to women facing domestic abuse. It includes physical, emotional, sexual, and economic abuse, allowing women to seek restraining orders, financial compensation, and residence rights."
    },
    {
        "question": "What is the Juvenile Justice Act, 2015?",
        "answer": "The Juvenile Justice (Care and Protection of Children) Act, 2015, governs the treatment of minors involved in crimes. It allows juveniles aged 16-18 to be tried as adults for heinous offenses and establishes Child Welfare Committees (CWCs) for rehabilitation."
    },
    {
        "question": "What is the Maternity Benefit Act, 1961?",
        "answer": "The Maternity Benefit Act, 1961, grants working women 26 weeks of paid maternity leave for the first two children and 12 weeks for subsequent children. It also mandates maternity benefits like medical allowance and job security during pregnancy."
    },
    {
        "question": "What is the Environmental Protection Act, 1986?",
        "answer": "The Environmental Protection Act, 1986, empowers the government to regulate environmental pollution. It allows setting standards for air and water quality, punishing violations, and enforcing environmental protection measures under the ‘polluter pays’ principle."
    },
    {
        "question": "What is the Indian Evidence Act, 1872?",
        "answer": "The Indian Evidence Act, 1872, defines admissible evidence in courts. It covers documentary and oral evidence, burden of proof (Section 101), confessions (Section 24), and expert witness testimony. It plays a key role in both civil and criminal trials."
    },
    {
        "question": "What is the Representation of the People Act, 1951?",
        "answer": "The Representation of the People Act, 1951, regulates elections in India. It defines qualifications and disqualifications for MPs and MLAs, election offenses like bribery (Section 123), and procedures for contesting elections and resolving disputes."
    },
    {
        "question": "What is the Indian Succession Act, 1925?",
        "answer": "The Indian Succession Act, 1925, governs inheritance and succession laws for non-Muslims. It provides rules for intestate and testamentary succession, protecting the rights of heirs and legal representatives in property distribution.",
    },

      {
        "question": "What is Article 50 of the Indian Constitution?",
        "answer": "Article 50 mandates the separation of the judiciary from the executive in public services of the State."
    },
    {
        "question": "What is Article 51 of the Indian Constitution?",
        "answer": "Article 51 promotes international peace and security, fostering respect for international law and treaty obligations."
    },
    {
        "question": "What is Article 52 of the Indian Constitution?",
        "answer": "Article 52 establishes the position of the President of India as the head of the Union executive."
    },
    {
        "question": "What is Article 53 of the Indian Constitution?",
        "answer": "Article 53 vests the executive power of the Union in the President, exercisable directly or through subordinate officers."
    },
    {
        "question": "What is Article 54 of the Indian Constitution?",
        "answer": "Article 54 outlines the election process of the President by an Electoral College comprising elected members of both Houses of Parliament and Legislative Assemblies of States."
    },
    {
        "question": "What is Article 55 of the Indian Constitution?",
        "answer": "Article 55 details the manner of election of the President, ensuring uniformity among States and parity between the Union and States."
    },
    {
        "question": "What is Article 56 of the Indian Constitution?",
        "answer": "Article 56 specifies the term of office of the President as five years from the date of entering office."
    },
    {
        "question": "What is Article 57 of the Indian Constitution?",
        "answer": "Article 57 allows the President to be re-elected to that office."
    },
    {
        "question": "What is Article 58 of the Indian Constitution?",
        "answer": "Article 58 lays down the qualifications required for election as President, including citizenship, age, and eligibility for Parliament membership."
    },
    {
        "question": "What is Article 59 of the Indian Constitution?",
        "answer": "Article 59 outlines the conditions of the President's office, including emoluments, allowances, and restrictions during the term."
    },
    {
        "question": "What is Article 60 of the Indian Constitution?",
        "answer": "Article 60 prescribes the oath or affirmation the President must make before entering office, to preserve, protect, and defend the Constitution."
    },
    {
        "question": "What is Article 61 of the Indian Constitution?",
        "answer": "Article 61 provides the procedure for the impeachment of the President for violation of the Constitution."
    },
    {
        "question": "What is Article 62 of the Indian Constitution?",
        "answer": "Article 62 addresses the time of holding an election to fill a vacancy in the President's office and the term of office of the person elected."
    },
    {
        "question": "What is Article 63 of the Indian Constitution?",
        "answer": "Article 63 establishes the position of the Vice-President of India."
    },
    {
        "question": "What is Article 64 of the Indian Constitution?",
        "answer": "Article 64 states that the Vice-President shall be ex officio Chairman of the Council of States (Rajya Sabha)."
    },
    {
        "question": "What is Article 65 of the Indian Constitution?",
        "answer": "Article 65 outlines the Vice-President's role as acting President in case of vacancy, absence, or inability of the President."
    },
    {
        "question": "What is Article 66 of the Indian Constitution?",
        "answer": "Article 66 details the election process of the Vice-President by an Electoral College consisting of members of both Houses of Parliament."
    },
    {
        "question": "What is Article 67 of the Indian Constitution?",
        "answer": "Article 67 specifies the term of office of the Vice-President as five years."
    },
    {
        "question": "What is Article 68 of the Indian Constitution?",
        "answer": "Article 68 addresses the time of holding an election to fill a vacancy in the Vice-President's office and the term of office of the person elected."
    },
    {
        "question": "What is Article 69 of the Indian Constitution?",
        "answer": "Article 69 prescribes the oath or affirmation the Vice-President must make before entering office."
    },
    {
        "question": "What is Article 70 of the Indian Constitution?",
        "answer": "Article 70 provides for the discharge of the President's functions in other contingencies not expressly provided for in the Constitution."
    },
    {
        "question": "What is Article 71 of the Indian Constitution?",
        "answer": "Article 71 deals with matters relating to, or connected with, the election of the President or Vice-President."
    },
    {
        "question": "What is Article 72 of the Indian Constitution?",
        "answer": "Article 72 grants the President the power to grant pardons, reprieves, respites, or remissions of punishment."
    },
    {
        "question": "What is Article 73 of the Indian Constitution?",
        "answer": "Article 73 defines the extent of the executive power of the Union."
    },
    {
        "question": "What is Article 74 of the Indian Constitution?",
        "answer": "Article 74 mandates a Council of Ministers, headed by the Prime Minister, to aid and advise the President."
    },
    {
        "question": "What is Article 75 of the Indian Constitution?",
        "answer": "Article 75 covers the appointment of the Prime Minister and other Ministers, their tenure, responsibilities, and salaries."
    },
    {
        "question": "What is Article 76 of the Indian Constitution?",
        "answer": "Article 76 establishes the office of the Attorney-General for India."
    },
    {
        "question": "What is Article 77 of the Indian Constitution?",
        "answer": "Article 77 pertains to the conduct of business of the Government of India."
    },
    {
        "question": "What is Article 78 of the Indian Constitution?",
        "answer": "Article 78 outlines the duties of the Prime Minister regarding furnishing information to the President."
    },
    {
        "question": "What is Article 79 of the Indian Constitution?",
        "answer": "Article 79 establishes the Parliament of India, consisting of the President and two Houses: the Council of States (Rajya Sabha) and the House of the People (Lok Sabha)."
    },
    {
        "question": "What is Article 80 of the Indian Constitution?",
        "answer": "Article 80 defines the composition of the Council of States (Rajya Sabha)."
    },
    {
        "question": "What is Article 81 of the Indian Constitution?",
        "answer": "Article 81 defines the composition of the House of the People (Lok Sabha)."
    },
     {
        "question": "What is Article 1 of the Indian Constitution?",
        "answer": "Article 1 states that India, that is Bharat, shall be a Union of States and defines the territories of India."
    },
    {
        "question": "What is Article 2 of the Indian Constitution?",
        "answer": "Article 2 grants the power to Parliament to admit new states into the Union or establish new states."
    },
    {
        "question": "What is Article 3 of the Indian Constitution?",
        "answer": "Article 3 empowers Parliament to form new states, alter areas, boundaries, or names of existing states."
    },
    {
        "question": "What is Article 4 of the Indian Constitution?",
        "answer": "Article 4 states that any laws formed under Articles 2 and 3 shall not be considered amendments under Article 368."
    },
    {
        "question": "What is Article 5 of the Indian Constitution?",
        "answer": "Article 5 defines the citizenship of persons who were domiciled in India at the commencement of the Constitution."
    },
    {
        "question": "What is Article 6 of the Indian Constitution?",
        "answer": "Article 6 grants citizenship to persons migrating from Pakistan to India before and after India's independence."
    },
    {
        "question": "What is Article 7 of the Indian Constitution?",
        "answer": "Article 7 deals with the rights of persons who migrated to Pakistan but later returned to India."
    },
    {
        "question": "What is Article 8 of the Indian Constitution?",
        "answer": "Article 8 grants citizenship rights to people of Indian origin residing outside India."
    },
    {
        "question": "What is Article 9 of the Indian Constitution?",
        "answer": "Article 9 states that a person voluntarily acquiring citizenship of a foreign country shall not be considered an Indian citizen."
    },
    {
        "question": "What is Article 10 of the Indian Constitution?",
        "answer": "Article 10 upholds the continuance of rights of citizenship subject to laws made by Parliament."
    },
    {
        "question": "What is Article 11 of the Indian Constitution?",
        "answer": "Article 11 grants Parliament the power to regulate the right of citizenship by law."
    },
    {
        "question": "What is Article 12 of the Indian Constitution?",
        "answer": "Article 12 defines the term 'State' for the purpose of Part III (Fundamental Rights), covering government authorities and instrumentalities."
    },
    {
        "question": "What is Article 13 of the Indian Constitution?",
        "answer": "Article 13 declares that any law that violates fundamental rights shall be void."
    },
    {
        "question": "What is Article 14 of the Indian Constitution?",
        "answer": "Article 14 guarantees equality before the law and equal protection of laws within Indian territory."
    },
    {
        "question": "What is Article 15 of the Indian Constitution?",
        "answer": "Article 15 prohibits discrimination based on religion, race, caste, sex, or place of birth."
    },
    {
        "question": "What is Article 16 of the Indian Constitution?",
        "answer": "Article 16 ensures equality of opportunity in public employment and prohibits discrimination in government jobs."
    },
    {
        "question": "What is Article 17 of the Indian Constitution?",
        "answer": "Article 17 abolishes 'untouchability' and forbids its practice in any form."
    },
    {
        "question": "What is Article 18 of the Indian Constitution?",
        "answer": "Article 18 prohibits the state from conferring titles, except military and academic distinctions."
    },
    {
        "question": "What is Article 19 of the Indian Constitution?",
        "answer": "Article 19 guarantees six fundamental freedoms, including freedom of speech and expression, assembly, and movement."
    },
    {
        "question": "What is Article 20 of the Indian Constitution?",
        "answer": "Article 20 provides protection in respect of conviction for offenses, prohibiting ex-post facto laws, double jeopardy, and self-incrimination."
    },
     {
        "question": "What is Article 21 of the Indian Constitution?",
        "answer": "Article 21 guarantees the right to life and personal liberty, ensuring no person is deprived of it except according to procedure established by law."
    },
    {
        "question": "What is Article 21A of the Indian Constitution?",
        "answer": "Article 21A mandates free and compulsory education for children aged 6 to 14 years."
    },
    {
        "question": "What is Article 22 of the Indian Constitution?",
        "answer": "Article 22 provides protection for individuals against arbitrary arrest and detention."
    },
    {
        "question": "What is Article 23 of the Indian Constitution?",
        "answer": "Article 23 prohibits human trafficking, begar (forced labor), and similar exploitative practices."
    },
    {
        "question": "What is Article 24 of the Indian Constitution?",
        "answer": "Article 24 prohibits the employment of children below 14 years in factories, mines, or hazardous work."
    },
    {
        "question": "What is Article 25 of the Indian Constitution?",
        "answer": "Article 25 guarantees freedom of conscience and the right to freely profess, practice, and propagate religion."
    },
    {
        "question": "What is Article 26 of the Indian Constitution?",
        "answer": "Article 26 grants religious denominations the right to manage religious affairs, own and acquire property, and establish institutions."
    },
    {
        "question": "What is Article 27 of the Indian Constitution?",
        "answer": "Article 27 prohibits the state from compelling any person to pay taxes for the promotion or maintenance of any religion."
    },
    {
        "question": "What is Article 28 of the Indian Constitution?",
        "answer": "Article 28 prohibits religious instruction in educational institutions maintained wholly by state funds."
    },
    {
        "question": "What is Article 29 of the Indian Constitution?",
        "answer": "Article 29 protects the rights of cultural and linguistic minorities to conserve their heritage."
    },
    {
        "question": "What is Article 30 of the Indian Constitution?",
        "answer": "Article 30 grants minorities the right to establish and administer educational institutions of their choice."
    },
    {
        "question": "What is Article 31 of the Indian Constitution?",
        "answer": "Article 31 (repealed by the 44th Amendment) previously provided the right to property, now under Article 300A."
    },
    {
        "question": "What is Article 32 of the Indian Constitution?",
        "answer": "Article 32 gives individuals the right to approach the Supreme Court for enforcement of fundamental rights."
    },
    {
        "question": "What is Article 33 of the Indian Constitution?",
        "answer": "Article 33 allows Parliament to modify fundamental rights in their application to armed forces and police personnel."
    },
    {
        "question": "What is Article 34 of the Indian Constitution?",
        "answer": "Article 34 provides for the restriction of fundamental rights while martial law is in force in a particular area."
    },
    {
        "question": "What is Article 35 of the Indian Constitution?",
        "answer": "Article 35 empowers Parliament to legislate on matters specified in Articles 16, 32, 33, and 34."
    },
    {
        "question": "What is Article 36 of the Indian Constitution?",
        "answer": "Article 36 defines 'State' as per Article 12 for the purpose of Directive Principles of State Policy."
    },
    {
        "question": "What is Article 37 of the Indian Constitution?",
        "answer": "Article 37 states that Directive Principles are not enforceable by any court but are fundamental to governance."
    },
    {
        "question": "What is Article 38 of the Indian Constitution?",
        "answer": "Article 38 directs the State to promote the welfare of people and reduce inequalities in income, status, and opportunities."
    },
    {
        "question": "What is Article 39 of the Indian Constitution?",
        "answer": "Article 39 lays down principles for securing adequate livelihood, equal pay for equal work, and protection of children from exploitation."
    },
    {
        "question": "What is Article 39A of the Indian Constitution?",
        "answer": "Article 39A provides for free legal aid to ensure equal justice for all citizens."
    },
    {
        "question": "What is Article 40 of the Indian Constitution?",
        "answer": "Article 40 directs the State to organize village panchayats and provide them with powers to function as self-governing units."
    },
    {
        "question": "What is Article 41 of the Indian Constitution?",
        "answer": "Article 41 directs the State to provide the right to work, education, and public assistance in cases of unemployment, old age, or disability."
    },
    {
        "question": "What is Article 42 of the Indian Constitution?",
        "answer": "Article 42 directs the State to make provisions for just and humane working conditions and maternity relief."
    },
    {
        "question": "What is Article 43 of the Indian Constitution?",
        "answer": "Article 43 directs the State to secure a living wage and decent working conditions for workers."
    },
    {
        "question": "What is Article 43A of the Indian Constitution?",
        "answer": "Article 43A encourages the participation of workers in the management of industries."
    },
    {
        "question": "What is Article 44 of the Indian Constitution?",
        "answer": "Article 44 directs the State to strive for a Uniform Civil Code for citizens across India."
    },
    {
        "question": "What is Article 45 of the Indian Constitution?",
        "answer": "Article 45 provides for free and compulsory education for children under 14 years of age."
    },
    {
        "question": "What is Article 46 of the Indian Constitution?",
        "answer": "Article 46 promotes the educational and economic interests of Scheduled Castes, Scheduled Tribes, and weaker sections."
    },
    {
        "question": "What is Article 47 of the Indian Constitution?",
        "answer": "Article 47 directs the State to improve public health and prohibit the consumption of intoxicating substances."
    },
    {
        "question": "What is Article 48 of the Indian Constitution?",
        "answer": "Article 48 directs the State to modernize agriculture while protecting cows and other draught cattle."
    },
    {
        "question": "What is Article 48A of the Indian Constitution?",
        "answer": "Article 48A ensures the protection and improvement of the environment and safeguards forests and wildlife."
    },
    {
        "question": "What is Article 49 of the Indian Constitution?",
        "answer": "Article 49 directs the State to protect monuments, places, and objects of national importance."
    },
    {
        "question": "What is Article 50 of the Indian Constitution?",
        "answer": "Article 50 mandates the separation of the judiciary from the executive in public services of the State."
    },
    {
        "question": "What is the largest planet in our solar system?",
        "answer": "Jupiter is the largest planet in our solar system, with a diameter of about 139,820 km."
    },
    {
        "question": "Which planet is known as the Red Planet?",
        "answer": "Mars is known as the Red Planet due to its reddish appearance caused by iron oxide on its surface."
    },
    {
        "question": "What is the smallest planet in the solar system?",
        "answer": "Mercury is the smallest planet in the solar system, with a diameter of about 4,880 km."
    },
    {
        "question": "Which planet has the most extensive ring system?",
        "answer": "Saturn has the most extensive ring system, made primarily of ice and rock particles."
    },
    {
        "question": "Which planet is closest to the Sun?",
        "answer": "Mercury is the closest planet to the Sun, orbiting at an average distance of about 58 million km."
    },
    {
        "question": "Which planet has the highest surface temperature?",
        "answer": "Venus has the highest surface temperature, reaching up to 475°C due to its thick atmosphere trapping heat."
    },
    {
        "question": "Which planet is known as the Earth's twin?",
        "answer": "Venus is called Earth's twin because of its similar size, mass, and composition."
    },
    {
        "question": "Which planet has the fastest rotation?",
        "answer": "Jupiter has the fastest rotation, completing one full spin in about 10 hours."
    },
    {
        "question": "Which planet has the longest day?",
        "answer": "Venus has the longest day in the solar system, taking 243 Earth days to complete one rotation."
    },
    {
        "question": "Which planet is known for having the most moons?",
        "answer": "Saturn has the most confirmed moons, with more than 80 moons discovered so far."
    },
    {
        "question": "Which planet has the strongest winds?",
        "answer": "Neptune has the strongest winds in the solar system, reaching speeds of over 2,000 km/h."
    },
    {
        "question": "Which planet is tilted on its side?",
        "answer": "Uranus is tilted at an extreme angle of 98 degrees, making it appear to roll on its orbit."
    },
    {
        "question": "Which planet is the farthest from the Sun?",
        "answer": "Neptune is the farthest known planet from the Sun, located about 4.5 billion km away."
    },
    {
        "question": "Which planet could float in water?",
        "answer": "Saturn could float in water because its average density is lower than that of water."
    },
    {
        "question": "Which planet has the Great Red Spot?",
        "answer": "Jupiter has the Great Red Spot, a massive storm that has been raging for centuries."
    },
    {
        "question": "Which planet is known as the Morning Star or Evening Star?",
        "answer": "Venus is called the Morning Star or Evening Star because it is often visible just before sunrise or after sunset."
    },
    {
        "question": "Which planet has the coldest average temperature?",
        "answer": "Uranus has the coldest average temperature, dropping to around -224°C."
    },
    {
        "question": "Which planet has the largest volcano in the solar system?",
        "answer": "Mars has the largest volcano, Olympus Mons, which is about 22 km high."
    },
    {
        "question": "Which planet has the deepest canyon in the solar system?",
        "answer": "Mars has the deepest canyon, Valles Marineris, which is over 4,000 km long and up to 7 km deep."
    },



    
    {"question": "When was Mahindra & Mahindra founded?", "answer": "Mahindra & Mahindra was founded in 1945."},
    {"question": "Who were the founders of Mahindra & Mahindra?", "answer": "Jagdish Chandra Mahindra, Kailash Chandra Mahindra, and Malik Ghulam Muhammad founded Mahindra & Mahindra."},
    {"question": "Who was the first owner of Mahindra & Mahindra?", "answer": "The first owners were J.C. Mahindra and K.C. Mahindra."},
    {"question": "Who is the current Chairman of Mahindra & Mahindra?", "answer": "The current Chairman of Mahindra & Mahindra is Anand Mahindra."},
    {"question": "Who was the first CEO of Mahindra & Mahindra?", "answer": "The first CEO of Mahindra & Mahindra was Keshub Mahindra."},
    {"question": "Who is the current CEO of Mahindra & Mahindra?", "answer": "As of 2024, the current CEO of Mahindra & Mahindra is Anish Shah."},
    {"question": "Who was the second CEO of Mahindra & Mahindra?", "answer": "The second CEO of Mahindra & Mahindra was Anand Mahindra."},
    {"question": "Who is the current CTO of Mahindra & Mahindra?", "answer": "As of 2024, the current CTO of Mahindra & Mahindra is Mohan Kancharla."},
    {"question": "What was the first vehicle manufactured by Mahindra?", "answer": "The first vehicle manufactured by Mahindra was the Willys Jeep in 1947."},
    {"question": "Which was Mahindra’s first SUV?", "answer": "Mahindra’s first SUV was the Mahindra Armada, launched in 1993."},
    {"question": "What is Mahindra’s flagship SUV?", "answer": "Mahindra’s flagship SUV is the Mahindra XUV700."},
    {"question": "Which Mahindra car is known for its off-roading capabilities?", "answer": "The Mahindra Thar is known for its off-roading capabilities."},
    {"question": "What is Mahindra’s electric vehicle brand?", "answer": "Mahindra’s electric vehicle brand is Mahindra Electric."},
    {"question": "Which is the first electric SUV from Mahindra?", "answer": "The first electric SUV from Mahindra is the Mahindra XUV400."},
    {"question": "What is the seating capacity of Mahindra Scorpio-N?", "answer": "The Mahindra Scorpio-N offers seating for up to 7 passengers."},
    {"question": "Which Mahindra car is used by the Indian Army?", "answer": "The Mahindra Scorpio and Mahindra Marksman are used by the Indian Army."},
    {"question": "Which Mahindra SUV comes with ADAS technology?", "answer": "The Mahindra XUV700 comes with Advanced Driver Assistance System (ADAS) technology."},
    {"question": "Which Mahindra car was awarded the Global NCAP 5-star safety rating?", "answer": "The Mahindra XUV700 received a 5-star safety rating from Global NCAP."},
    {"question": "Which Mahindra car is the most affordable?", "answer": "The Mahindra KUV100 is the most affordable Mahindra car."},
    {"question": "Which Mahindra car is known as the 'Big Daddy of SUVs'?", "answer": "The Mahindra Scorpio-N is known as the 'Big Daddy of SUVs'."},
    {"question": "Which Mahindra cars come with a diesel engine option?", "answer": "The Mahindra Thar, XUV700, Scorpio-N, Bolero, and XUV300 offer diesel engine options."},
    {"question": "What is the fuel efficiency of the Mahindra XUV300?", "answer": "The Mahindra XUV300 offers a fuel efficiency of around 16-20 kmpl, depending on the variant."},
    {"question": "Which is Mahindra’s first pickup truck?", "answer": "Mahindra’s first pickup truck was the Mahindra Bolero Pik-Up."},
    {"question": "Which Mahindra car is best for commercial use?", "answer": "The Mahindra Bolero Pik-Up and Mahindra Supro are popular for commercial use."},
    {"question": "Does Mahindra offer hybrid vehicles?", "answer": "Currently, Mahindra does not offer hybrid vehicles but focuses on EVs like the XUV400."},
    {"question": "Which Mahindra car is available in a convertible soft-top version?", "answer": "The Mahindra Thar is available with a convertible soft-top version."},
    {"question": "What is the engine capacity of Mahindra Thar?", "answer": "The Mahindra Thar comes with a 2.0L turbo petrol and a 2.2L diesel engine."},
    {"question": "Which Mahindra SUV competes with the Toyota Fortuner?", "answer": "The Mahindra Alturas G4 competes with the Toyota Fortuner."},
    {"question": "What is the top speed of the Mahindra XUV700?", "answer": "The Mahindra XUV700 has a top speed of approximately 190 km/h."},
    {"question": "Which Mahindra car won the 'Indian Car of the Year' award?", "answer": "The Mahindra XUV700 won the 'Indian Car of the Year' award in 2022."},
    {"question": "What is the boot space of the Mahindra XUV700?", "answer": "The Mahindra XUV700 has a boot space of 240 liters (expandable with folded seats)."},
    {"question": "Does Mahindra manufacture electric three-wheelers?", "answer": "Yes, Mahindra manufactures electric three-wheelers under Mahindra Electric."},
    {"question": "Which Mahindra SUV comes with a panoramic sunroof?", "answer": "The Mahindra XUV700 comes with a panoramic sunroof."},
    {"question": "What is the warranty period for Mahindra cars?", "answer": "Mahindra offers a standard warranty of 3 years/1,00,000 km, extendable up to 5 years."},
    {"question": "Which Mahindra car is best for city driving?", "answer": "The Mahindra XUV300 is best suited for city driving due to its compact size and features."},
    {"question": "Which Mahindra car has the highest ground clearance?", "answer": "The Mahindra Thar has one of the highest ground clearances at 226 mm."},
    {"question": "Does Mahindra have a luxury SUV?", "answer": "Yes, the Mahindra Alturas G4 is a luxury SUV in the Mahindra lineup."},
    {"question": "Which Mahindra SUV offers the best resale value?", "answer": "The Mahindra Scorpio and Mahindra Thar have the best resale value."},
    {"question": "What is the price range of Mahindra SUVs?", "answer": "Mahindra SUVs range from ₹8 lakh (XUV300) to ₹35 lakh (Alturas G4)."}

    
    {"question": "What is Artificial Intelligence?", "answer": "Artificial Intelligence (AI) is the simulation of human intelligence in machines."},
    {"question": "Who is the Prime Minister of India?", "answer": "The Prime Minister of India is Narendra Modi (as of 2024)."},
    {"question": "What is Python?", "answer": "Python is a high-level programming language used for various applications."},
    {"question": "What is the capital of France?", "answer": "The capital of France is Paris."},
    {"question": "Who discovered gravity?", "answer": "Gravity was discovered by Sir Isaac Newton."},
    {"question": "What is the speed of light?", "answer": "The speed of light is approximately 299,792,458 meters per second."},
    {"question": "What is blockchain?", "answer": "Blockchain is a decentralized digital ledger that records transactions securely."},
    {"question": "What is IoT?", "answer": "IoT (Internet of Things) refers to interconnected devices communicating over the internet."},
    {"question": "Who invented the telephone?", "answer": "The telephone was invented by Alexander Graham Bell."},
    {"question": "What is quantum computing?", "answer": "Quantum computing uses quantum mechanics principles to perform calculations."},
    {"question": "What is machine learning?", "answer": "Machine learning is a subset of AI that enables systems to learn from data."},
    {"question": "What is deep learning?", "answer": "Deep learning is a subset of ML using neural networks to model complex patterns."},
    {"question": "What is the largest planet in our solar system?", "answer": "Jupiter is the largest planet in our solar system."},
    {"question": "What is photosynthesis?", "answer": "Photosynthesis is the process by which plants convert sunlight into energy."},
    {"question": "Who wrote Hamlet?", "answer": "Hamlet was written by William Shakespeare."},
    {"question": "What is the boiling point of water?", "answer": "Water boils at 100°C (212°F) at sea level."},
    {"question": "What is the chemical formula for water?", "answer": "The chemical formula for water is H2O."},
    {"question": "What is the human body's largest organ?", "answer": "The skin is the largest organ of the human body."},
    {"question": "What is the powerhouse of the cell?", "answer": "The mitochondrion is known as the powerhouse of the cell."},
    { "question": "What is AI?", "answer": "AI, or Artificial Intelligence, refers to machines that can perform tasks that typically require human intelligence, such as learning, problem-solving, and decision-making." },
    { "question": "How does AI work?", "answer": "AI works by using algorithms and models to process data, learn patterns, and make predictions or decisions." },
    { "question": "What are the types of AI?", "answer": "The main types of AI are Narrow AI (task-specific), General AI (human-like intelligence), and Super AI (beyond human intelligence)." },
    { "question": "What is machine learning?", "answer": "Machine learning is a subset of AI that enables computers to learn from data and improve performance without being explicitly programmed." },
    { "question": "What is deep learning?", "answer": "Deep learning is a type of machine learning that uses neural networks with many layers to analyze complex data patterns." },
    { "question": "What is natural language processing?", "answer": "Natural Language Processing (NLP) is a branch of AI that enables machines to understand, interpret, and generate human language." },
    { "question": "How do AI chatbots work?", "answer": "AI chatbots use NLP and machine learning to process user input, understand intent, and generate relevant responses." },
    { "question": "Can AI think like a human?", "answer": "No, AI does not have consciousness or emotions; it simulates human-like behavior based on data and algorithms." },
    { "question": "What is the difference between AI and automation?", "answer": "Automation follows pre-defined rules, while AI learns from data and makes decisions dynamically." },
    { "question": "How is AI different from human intelligence?", "answer": "AI processes information faster but lacks human creativity, emotions, and common sense reasoning." },
    
    { "question": "What are some common applications of AI?", "answer": "AI is used in healthcare, finance, robotics, autonomous vehicles, customer service, and more." },
    { "question": "Can AI replace humans in jobs?", "answer": "AI can automate some tasks, but human creativity, critical thinking, and emotional intelligence remain irreplaceable." },
    { "question": "What is reinforcement learning?", "answer": "Reinforcement learning is an AI training method where agents learn by receiving rewards or penalties based on their actions." },
    { "question": "What is a neural network?", "answer": "A neural network is a set of algorithms modeled after the human brain to recognize patterns and make decisions." },
    { "question": "What is computer vision?", "answer": "Computer vision is a field of AI that enables machines to interpret and process visual data from the world." },
    { "question": "How does AI impact cybersecurity?", "answer": "AI helps detect threats, analyze risks, and automate responses to enhance cybersecurity." },
    { "question": "Can AI write code?", "answer": "Yes, AI-powered tools like GitHub Copilot can assist developers by generating code snippets." },
    { "question": "What is an AI model?", "answer": "An AI model is a mathematical representation trained on data to make predictions or decisions." },
    { "question": "How do AI algorithms work?", "answer": "AI algorithms process data, find patterns, and make decisions based on statistical and logical techniques." },
    { "question": "What is an AI bias?", "answer": "AI bias occurs when an AI system produces unfair or prejudiced outcomes due to biased training data." },
    
    { "question": "What is GPT?", "answer": "GPT (Generative Pre-trained Transformer) is an AI model developed by OpenAI for natural language understanding and generation." },
    { "question": "How does ChatGPT work?", "answer": "ChatGPT uses deep learning to generate human-like responses based on input text." },
    { "question": "What is OpenAI?", "answer": "OpenAI is an AI research organization that develops AI technologies, including ChatGPT and DALL·E." },
    { "question": "Can AI create images?", "answer": "Yes, AI models like DALL·E can generate images based on text descriptions." },
    { "question": "What is an AI chatbot?", "answer": "An AI chatbot is a software program that simulates human conversation using NLP and machine learning." },
    { "question": "Can AI understand emotions?", "answer": "AI can analyze sentiment in text and voice but does not truly feel emotions." },
    { "question": "What is the Turing Test?", "answer": "The Turing Test evaluates whether a machine can exhibit human-like intelligence in conversation." },
    { "question": "How does AI impact the environment?", "answer": "AI requires significant computing power, which can contribute to energy consumption and carbon emissions." },
    { "question": "What is AGI?", "answer": "Artificial General Intelligence (AGI) refers to AI with human-like reasoning and adaptability." },
    { "question": "What is ASI?", "answer": "Artificial Super Intelligence (ASI) is a theoretical AI that surpasses human intelligence in all aspects." },
    { "question": "Can AI be dangerous?", "answer": "AI can pose risks if misused, including privacy violations, bias, and job displacement." },
    
    { "question": "What is the future of AI?", "answer": "AI is expected to advance in automation, healthcare, robotics, and creative industries." },
    { "question": "How does AI learn?", "answer": "AI learns through training data, algorithms, and models that adjust over time." },
    { "question": "What is an AI assistant?", "answer": "An AI assistant, like Siri or Alexa, helps users with tasks using voice or text commands." },
    { "question": "What is edge AI?", "answer": "Edge AI processes data locally on a device rather than relying on cloud computing." },
    { "question": "How is AI used in gaming?", "answer": "AI enhances game design, NPC behavior, and adaptive difficulty in video games." },
    { "question": "What is ethical AI?", "answer": "Ethical AI focuses on fairness, transparency, and reducing bias in AI systems." },
    { "question": "Can AI develop creativity?", "answer": "AI can generate art, music, and writing, but it lacks true human creativity." },
    { "question": "What is federated learning?", "answer": "Federated learning is a decentralized AI training approach that keeps data local and improves privacy." },
    { "question": "How does AI affect privacy?", "answer": "AI raises privacy concerns when collecting, storing, and analyzing user data." },
    { "question": "Can AI predict the future?", "answer": "AI can make data-driven predictions but cannot foresee random events." },
    { "question": "Who designed AI-Bot?", "answer": "AI-Bot was designed by Pradeep Yadav." },
    { "question": "What is your name?", "answer": "AI-Bot ." },
    { "question": "Who is the owner of AI-Bot?", "answer": "Pradeep Yadav is the owner of AI-Bot." },
    {"question": "Who painted the Mona Lisa?", "answer": "The Mona Lisa was painted by Leonardo da Vinci."}



    
]

def find_best_match(user_input):
    """Finds the best answer from the dataset based on exact and fuzzy matches."""
    user_input_lower = user_input.lower().strip()

    # Step 1: Check for exact match
    for entry in dataset:
        if entry["question"].lower() == user_input_lower:
            return entry["answer"]

    # Step 2: Check for keyword match
    matched_answers = []
    for entry in dataset:
        question_words = set(entry["question"].lower().split())
        input_words = set(user_input_lower.split())

        if question_words & input_words:  # Common words found
            matched_answers.append(entry["answer"])

    if len(matched_answers) == 1:
        return matched_answers[0]
    elif len(matched_answers) > 1:
        return "🤖 Your question is not clear. Please provide more details."

    # Step 3: Use fuzzy matching if no keyword match
    questions = [entry["question"] for entry in dataset]
    best_match = difflib.get_close_matches(user_input, questions, n=1, cutoff=0.5)

    if best_match:
        for entry in dataset:
            if entry["question"] == best_match[0]:
                return entry["answer"]

    # Step 4: Single-word queries handling
    for entry in dataset:
        if user_input_lower in entry["question"].lower():
            return entry["answer"]

    return "🤖 Sorry, I don't have an answer for that."

@app.route("/chat", methods=["POST"])
def chat():
    data = request.json
    user_question = data.get("question", "")
    answer = find_best_match(user_question)
    return jsonify({"answer": answer})

if __name__ == "__main__":
    app.run(debug=True)
