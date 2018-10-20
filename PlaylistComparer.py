import datetime
import os.path


def compare(path, old_playlists, new_playlists):
    path = os.path.join(path, "playlists_archive_" + datetime.date.today().strftime("%m%d%Y") + "_analysis.txt")
    with open(path, "w", encoding="utf-8", newline="") as file:

        file.write("#########\r\n")
        file.write("Playlists\r\n")
        file.write("#########\r\n")
        file.write("\r\n")

        for old_playlist in old_playlists:
            for new_playlist in new_playlists:
                if new_playlist.name == old_playlist.name:
                    break
            else:
                file.write("\t- " + old_playlist.name + "\r\n")

        for new_playlist in new_playlists:
            for old_playlist in old_playlists:
                if new_playlist.name == old_playlist.name:
                    break
            else:
                file.write("\t+ " + new_playlist.name + "\r\n")

        file.write("\r\n")
        file.write("#####\r\n")
        file.write("Songs\r\n")
        file.write("#####\r\n")
        file.write("\r\n")

        for new_playlist in new_playlists:
            file.write(new_playlist.name + "\r\n")
            file.write("\r\n")
            for old_playlist in old_playlists:
                if new_playlist.name == old_playlist.name:
                    for old_song in old_playlist.songs:
                        for new_song in new_playlist.songs:
                            if new_song.identifier == old_song.identifier or \
                               (new_song.title == old_song.title and new_song.artist == old_song.artist):
                                break
                        else:
                            file.write("\t- "
                                       + old_song.title
                                       + " : "
                                       + old_song.artist
                                       + "\r\n")

                    for old_song in old_playlist.songs:
                        for new_song in new_playlist.songs:
                            if new_song.identifier != old_song.identifier and \
                               new_song.title == old_song.title and \
                               new_song.artist == old_song.artist:
                                file.write("\t* "
                                           + new_song.title
                                           + " : "
                                           + new_song.artist
                                           + "\r\n")

                    for new_song in new_playlist.songs:
                        for old_song in old_playlist.songs:
                            if new_song.identifier == old_song.identifier or \
                               (new_song.title == old_song.title and new_song.artist == old_song.artist):
                                break
                        else:
                            file.write("\t+ "
                                       + new_song.title
                                       + " : "
                                       + new_song.artist
                                       + "\r\n")
            file.write("\r\n")

        file.write("##########\r\n")
        file.write("Duplicates\r\n")
        file.write("##########\r\n")
        file.write("\r\n")

        for new_playlist in new_playlists:
            file.write(new_playlist.name + "\r\n")
            file.write("\r\n")
            skip = []
            count1 = 0
            for new_song1 in new_playlist.songs:
                count2 = 0
                for new_song2 in new_playlist.songs:
                    if count1 not in skip and count2 not in skip and count1 != count2 and \
                       (new_song1.identifier == new_song2.identifier or
                            (new_song1.title == new_song2.title and new_song1.artist == new_song2.artist)):
                        skip.append(count1)
                        skip.append(count2)
                        file.write("\t"
                                   + new_song1.title
                                   + " : "
                                   + new_song1.artist
                                   + "\r\n")
                    count2 = count2 + 1
                count1 = count1 + 1
            file.write("\r\n")

        file.write("#########\r\n")
        file.write("Hierarchy\r\n")
        file.write("#########\r\n")
        file.write("\r\n")

        for parent_playlist in new_playlists:
            if "/" not in parent_playlist.name:
                file.write(parent_playlist.name + "\r\n")
                file.write("\r\n")
                parent_song_found = []
                has_child = False
                for child_playlist in new_playlists:
                    if parent_playlist.name != child_playlist.name and \
                       ((parent_playlist.name == "All" and "/" not in child_playlist.name) or
                            (parent_playlist.name != "All" and child_playlist.name.startswith(parent_playlist.name))):
                        has_child = True
                        for child_song in child_playlist.songs:
                            parent_count = 0
                            for parent_song in parent_playlist.songs:
                                if child_song.identifier == parent_song.identifier:
                                    parent_song_found.append(parent_count)
                                    break
                                parent_count = parent_count + 1
                            else:
                                file.write("\t- "
                                           + child_song.title
                                           + " : "
                                           + child_song.artist
                                           + " : "
                                           + child_playlist.name
                                           + "\r\n")
                if has_child:
                    parent_count = 0
                    for parent_song in parent_playlist.songs:
                        if parent_count not in parent_song_found:
                            file.write("\t+ "
                                       + parent_song.title
                                       + " : "
                                       + parent_song.artist
                                       + " : "
                                       + parent_playlist.name
                                       + "\r\n")
                        parent_count = parent_count + 1
                file.write("\r\n")

    return
