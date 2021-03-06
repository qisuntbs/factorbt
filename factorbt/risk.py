import numpy as np
from scipy import linalg


class risk_model():
    # BARRA-style risk models
    # including: statistical, fundamental, and macro
    @staticmethod
    def statistical(raw_ret, cov=None, K=7):
        # statistical risk model
        # K - Number of the principle components
        # Demean:
        if cov is None:
            print("generating covariance from the raw return inputs")
            assert (type(raw_ret) == np.array), "Raw return input has to be np.array"
            ret = raw_ret - raw_ret.mean(axis=0)
            cov = np.cov(ret.T)
        # eigen decomposition derivation:
        # http://fourier.eng.hmc.edu/e176/lectures/algebra/node9.html
        # use scipy.linalg.eigh (instead of np.linalg.eig)
        # to get rid of the complex number:
        w, v = linalg.eigh(cov)
        w_index = w.argsort()[::-1]  # from largest to smallest
        w_first_K = w[w_index[:K]]
        v_first_K = v[:, w_index[:K]]
        # V * diag(\lambda) * V.T:
        cov_eigen_decomp = np.matmul(np.matmul(v_first_K, np.diag(w_first_K)),
                                     v_first_K.T)
        # There is another approach:
        # https://ocw.mit.edu/courses/mathematics/18-s096-topics-in-mathematics-with-applications-in-finance-fall-2013/lecture-notes/MIT18_S096F13_lecnote15.pdf
        return cov_eigen_decomp + np.diag(np.diag(cov) - np.diag(cov_eigen_decomp))

    @staticmethod
    def fundamental(raw_ret, factor_data):
        # r = Xf + u
        # cov = X * F * X.T + \Delta
        pass
