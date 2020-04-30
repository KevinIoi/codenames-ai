#include <mlpack/core.hpp>
#include <string>

using namespace std;
using namespace mlpack;

int main(int argc, char const *argv[])
{

	int n_size = 3;

	arma::mat data;

	data::Load("resources/test.csv", data, true);

	mlpack::NeighborSearch<NearestNeighborSort, IPMetric<CosineDistance>> nn(data);

	arma::Mat<size_t> neighbors;
	arma::mat distances;

// 	ifstream fp("resources/testembed.txt");

// 	// split input
// 	istringstream iss(fp);

// std::vector<std::string> results(std::istream_iterator<std::string>{iss},
//                                  std::istream_iterator<std::string>());
	return 0;
}
