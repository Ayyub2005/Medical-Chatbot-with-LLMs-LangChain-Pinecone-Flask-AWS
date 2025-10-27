from setuptools import find_packages,setup

setup(
    name='medical_chatbot',
    version='0.1',
    author='Ayyub Hameem',
    author_email='ayyubhameem@gmail.com',
    packages=find_packages(),
    install_requires=[],
    description='A Medical Chatbot using LLMs, LangChain, Pinecone, Flask, and AWS',
)