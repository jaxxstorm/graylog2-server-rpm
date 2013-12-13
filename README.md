graylog2-server
===============

Graylog2 Server RPM packages


Releases
=============

A compiled RPM is available from the [releases page](https://github.com/jaxxstorm/graylog2-server-rpm/releases)

Installing
=============

This RPM requires some config after install. You'll need to ensure you have [elasticsearch 0.90.7](http://www.elasticsearch.org/download/) running and mongodb should be installed.

Once these are running, edit the config values in /etc/graylog2/server.conf and run the start script 
```
/etc/init.d/graylog2-server star
```

You can test your config values by running

```
java -jar /opt/graylog2/graylog2-server.jar -f /etc/graylog2/server.conf
```

Build your own
=============

building your own is simple
```
git clone https://github.com/jaxxstorm/graylog2-server-rpm.git ~/rpmbuild
cd rpmbuild && rpmbuild -ba SPECS/graylog2-server.spec
```

Patches
=============

These rpms have been tested extensively on my personal CentOS instance, however I realise they aren't perfect.
Please submit a pull request to improve them!


Acknowledgements
=============

Thanks to [Tavisto](https://github.com/tavisto/elasticsearch-rpms) for his excellent work on the elasticsearch rpm, was a great starting point for init scripts
and spec files

Thanks to the [graylog2](https://github.com/graylog2) team for making such an awesome open source product!

