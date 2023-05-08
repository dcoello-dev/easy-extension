#include <nlohmann/json.hpp>
#include <string>

using json = nlohmann::json;

struct Dummy {
    int a =0;
    int b = 1;
};

class ExampleInterface
{
public:
    virtual json metodo_uno(int a) const noexcept = 0;
    virtual json metodo_dos(float a, std::string b) const noexcept = 0;
    virtual json metodo_tres(const Dummy & input) const noexcept = 0;
    virtual Dummy metodo_cuatro(const Dummy & input) const noexcept = 0;
    virtual int metodo_cinco(int a) const noexcept = 0;
};