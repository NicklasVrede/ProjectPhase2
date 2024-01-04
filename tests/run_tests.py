import unittest


if __name__ == "__main__":
    # Start test discovery from the current directory, 
    # with the default pattern "test*.py"
    loader = unittest.TestLoader()
    start_dir = '.'
    suite = loader.discover(start_dir)

    runner = unittest.TextTestRunner()
    runner.run(suite)