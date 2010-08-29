File and media handling
=========================

TODO

Static files
----------------

Static files are those distributed with builds. They have very long cache time; they are, however, purged with every build.

There are plans for shared, never-to-expire CDN (like, say, javascript libraries that are always in for library-version-min.js).

Media files
---------------

Media files are those that are uploaded by user: pictures, avatars and friends. They should be shared across all servers and they should play nicely with reusable apps. Thus, they use default MEDIA_URL and MEDIA_ROOT settings.

We currently do not have cookie-less domain, so we'll just use cdn.rpgplanet.cz. cdn will probably be used for shared statics.

As we share database, we shall hope for non-interfering uploads in shared MEDIA_ROOT, defined in rpgcommon. God is with us.

There is WIP project called "treasury": each user has quota for uploading files. Those can be then linked/shared/embedded into articles. It's up to user how he will handle it (I'd put 5MB per user by default, allow embedding via oembed to use flickr or similar; paying users will of course has more. Using rsync to revy will help us put it out of our expensive scsi disks...or shall we use S3 from the start?).

