import factory
import factory.random
from factory.django import DjangoModelFactory

from folder.models import folder
from profile.models import Profile, User
factory.random.reseed_random('BHFOjfjeorhg')

class UserFactory(DjangoModelFactory):
    class Meta:
        model = User
    
    class Params:
        meta_prof = factory.Faker('profile')

    username = factory.LazyAttribute(lambda obj: obj.meta_prof['username'])
    email = factory.LazyAttribute(lambda obj: obj.meta_prof['mail'])
    first_name = factory.LazyAttribute(lambda obj: obj.meta_prof['name'].split()[0])
    last_name = factory.LazyAttribute(lambda obj: obj.meta_prof['name'].split()[1])
    password = factory.Faker('password')

class ProfileFactory(DjangoModelFactory):
    class Meta:
        model = Profile

    user = factory.SubFactory(UserFactory)
    
class folderFactory (DjangoModelFactory):
    class Meta:
        model = folder


    folder_headline = factory.Faker("sentence")
    pointer_url = factory.Faker("url")
    # pointer_question_id = factory.Faker("random_int")

    type_of_folder_char = factory.Faker("random_element",
        elements=('T', 'B', 'O', 'S', 'U'))

    # img_url = factory.Faker('image_url') !!! Must be Changed

    author = factory.SubFactory(ProfileFactory) # change to relative
    expected_reward = factory.Faker("random_int")
    total_questions = factory.Faker("random_int")
    total_pass = factory.Faker("random_int") 
    total_writes = factory.Faker("random_int") 

