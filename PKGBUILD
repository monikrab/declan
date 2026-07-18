pkgname=declan
pkgver=1.0
pkgrel=1
pkgdesc="Tiny utility to manage Arch Linux declaratively"
arch=('any')
url="https://github.com/monikrab/declan"
license=('GPL-2.0')
depends=('python' 'git')
optdepends=(
    'yay: for declan relay and declan rebuild'
    'pv: for declan backup'
    'github-cli: for declan rice'
)
source=(
    "https://github.com/monikrab/declan/archive/refs/tags/v${pkgver}.tar.gz"
)
sha256sums=('48122c2aa73f548f2e535aec2e807553b618abd21be274d7c1c55ba477b65684')

package() {
    install -Dm755 \
        "$srcdir/$pkgname-$pkgver/src/declan.py" \
        "$pkgdir/usr/bin/declan"

    install -Dm644 \
        "$srcdir/$pkgname-$pkgver/declan.1" \
        "$pkgdir/usr/share/man/man1/declan.1"
}
