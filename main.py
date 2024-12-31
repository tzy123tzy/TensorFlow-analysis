import analyse_contributors as ac
import analyse_releases as ar


def main():
    owner = 'tensorflow'
    repo = 'tensorflow'
    ac.analyse_contributors(owner, repo)
    ar.analyse_releases(owner, repo)
    print("new Push")


if __name__ == '__main__':
    main()
