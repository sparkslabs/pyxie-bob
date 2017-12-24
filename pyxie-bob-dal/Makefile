
all:
	@echo "clean - clean space as usual"
	@echo "deb - build a debian package"
	@echo "use - use the debian package"
	@echo "package - Package the dal code for windows/mac"

clean:
	rm -f ../pyxie-bob-dal_*.tar.gz ../pyxie-bob-dal_*.deb ../pyxie-bob-dal_*.dsc ../pyxie-bob-dal_*.build ../pyxie-bob-dal_*.changes ../pyxie-bob-dal_*.tar.gz PyxieBob.zip
	dh_clean

cleanslate:
	rm -f ../pyxie-bob-dal_*.tar.gz ../pyxie-bob-dal_*.deb ../pyxie-bob-dal_*.dsc ../pyxie-bob-dal_*.build ../pyxie-bob-dal_*.changes ../pyxie-bob-dal_*.tar.gz PyxieBob.zip
	dh_clean
	sudo dpkg --purge pyxie-bob-dal

deb:
	debuild -uc -us

use: deb
	sudo dpkg -i ../pyxie-bob-dal_*.deb

reuse: deb
	sudo dpkg --purge pyxie-bob-dal
	debuild -uc -us
	sudo dpkg -i ../pyxie-bob-dal_*.deb

package:
	@echo "Make a zip file suitable for use with Windows/Mac"
	ln -s libraries/PyxieBob/ PyxieBob
	zip -r PyxieBob.zip PyxieBob
	rm PyxieBob
