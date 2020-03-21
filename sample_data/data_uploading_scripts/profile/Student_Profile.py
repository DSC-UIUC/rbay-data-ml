import random
import decimal

"""professor_profile = {
    "Name": "Margaret Fleck",
    "Department/University": random.choice(dep),
    "Interest/Field": [random.choice(research_interests), random.choice(research_interests)],
    #"Postings":
    "Bio": "I'm a Research Associate Professor in the Department of Computer Science, University of Illinois, "
           "Urbana-Champaign. "
           "My research interests include computational linguistics, computer vision, and programming language tools "
           "to support language and vision research. "
           "Right now, I'm working on unsupervised algorithms that learn word "
           "boundaries from transcribed speech."
}"""

class Student_Profile(object):
    def __init__(self, name):
        self.name = name
        majors_list = [line.rstrip('\n') for line in open("data/majors_list.txt")]
        self.major = random.choice(majors_list)
        year = ["Freshman", "Sophomore", "Junior", "Senior"]
        self.year = random.choice(year)
        self.gpa = float(decimal.Decimal(random.randrange(230, 400)) / 100)
        courses = {
        "Computer Science": ["Software Design", "Discrete Structures", "Data Structures", "Computer Architecture",
                         "System Programming", "Numerical Methods",
                         "Introduction to Algorithms & Models of Computation",
                         "Data Mining", "Programming Language and Compilers", "Artificial Intelligence",
                         "Machine Learning", "Algorithms", "Parallel Programming", "Database Systems"],
        "Mathematics": ["Linear Algebra", "Multi-variable Calculus", "Differential Equations", "Graph Theory",
                    "Numerical Methods", "Intro to Combinatorics", "Euclidean Geometry", "Abstract Algebra",
                    "Numerical Analysis", "Complex Variables", "Probability Theory", "Linear Programming", "Algorithms",
                    "Real Analysis", "Set Theory and Topology"]
        }
        self.coursework = [random.choice(courses.get("Computer Science")), random.choice(courses.get("Computer Science")),
                   random.choice(courses.get("Mathematics")), random.choice(courses.get("Mathematics")),
                   random.choice(courses.get("Mathematics"))]
        bios = [line.rstrip('\n') for line in open("data/bios_c.txt")]
        self.bio = random.choice(bios)
        research_interests = [line.rstrip('\n') for line in open("data/research_interests.txt")]
        self.interests = [random.choice(research_interests), random.choice(research_interests), random.choice(research_interests)]
        technical_skills = [line.rstrip('\n') for line in open("data/technical_skills.txt")]
        self.skills = [random.choice(technical_skills), random.choice(technical_skills), random.choice(technical_skills)]
    
    @staticmethod
    def from_dict(source):
        pass

    def to_dict(self):
        ret = {
            'Name': self.name,
            'Major': self.major, 
            'Year' : self.year,
            'GPA' : self.gpa,
            'Courswork' : self.coursework,
            'Bio' : self.bio,
            'Interests' : self.interests,
            'Skills' : self.skills
        }

        return ret

    def __repr__(self):
        return(
            u'studentprofile(name={}, major={}, year={}, gpa={}, coursework={}, bio={}, interests={}, skills={})'
            .format(self.name, self.major, self.year, self.gpa, self.coursework, self.bio, self.interests,
                    self.skills))